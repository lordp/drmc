from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from drmc.db import get_db

bp = Blueprint("avail", __name__, url_prefix="/drmc/availability")


@bp.route("/", methods=["GET"])
def availability():
    db = get_db()

    players = db.execute(
        """
            SELECT p.name, GROUP_CONCAT(DISTINCT pa.availability) AS availability
            FROM players AS p 
            INNER JOIN player_availability AS pa ON pa.player_id = p.id
            GROUP BY p.id
            ORDER BY p.name
        """
    ).fetchall()

    player_availability = {}

    for player in players:
        if player["availability"]:
            player_availability[player["name"]] = [
                avail for avail in player["availability"].split(",")
            ]
        else:
            player_availability[player["name"]] = []

    print(player_availability)

    return render_template(
        "availability.html",
        availability=player_availability,
    )


@bp.route("/new", methods=["GET", "POST"])
@bp.route("/edit/<name>", methods=["GET", "POST"])
def change(name=None):
    db = get_db()

    if request.method == "POST":
        name = request.form.get("name")
        at_raid = request.form.get("at_raid")
        availability = request.form.getlist("availability")

        # try inserting into the player table
        row = db.execute(
            "INSERT INTO players (name) VALUES (?) ON CONFLICT DO NOTHING RETURNING id",
            (name,),
        ).fetchone()

        # get the new id if successful or retrieve the already existing id
        if row:
            (player_id,) = row
        else:
            (player_id,) = db.execute(
                "SELECT id FROM players WHERE name = ?", (name,)
            ).fetchone()

        # remove known availability settings and add new ones
        db.execute("DELETE FROM player_availability WHERE player_id = ?", (player_id,))

        for avail in availability:
            db.execute(
                "INSERT INTO player_availability (player_id, availability) VALUES (?, ?)",
                (player_id, avail),
            )

        # can this player do enchanting/alchemy at raid?
        if at_raid:
            db.execute(
                "INSERT INTO player_availability (player_id, availability) VALUES (?, ?)",
                (player_id, "at_raid"),
            )

        db.commit()

        flash("New availability settings added", "positive")

        return redirect("/drmc/availability")

    player_availability = []
    player_name = ""

    if name:
        player = db.execute(
            """
                SELECT p.name, GROUP_CONCAT(DISTINCT pa.availability) AS availability
                FROM players AS p
                INNER JOIN player_availability AS pa ON pa.player_id = p.id
                WHERE LOWER(p.name) = ?
                GROUP BY p.id
            """,
            (name,),
        ).fetchone()

        player_name = player["name"]

        if player["availability"]:
            player_availability = [avail for avail in player["availability"].split(",")]

    return render_template(
        "alter_availability.html",
        name=player_name,
        availability=player_availability,
    )
