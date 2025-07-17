from flask import (
    Blueprint,
    flash,
    g,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from drmc.db import get_db
from drmc import get_recipes, get_known_recipes, update_known_recipes

bp = Blueprint("tailor", __name__, url_prefix="/drmc/tailoring")


@bp.route("/", methods=["GET"])
def tailoring():
    db = get_db()
    recipes = get_recipes(db, "tailoring")
    players = get_known_recipes(db, "tailoring")

    player_recipes = {}
    player_availability = {}

    for player in players:
        if player["recipes"]:
            player_recipes[player["name"]] = [
                int(recipe) for recipe in player["recipes"].split(",")
            ]

    return render_template(
        "profession.html",
        profession="tailoring",
        recipes=recipes,
        players=player_recipes,
        player_count=len(players) + 1,
    )


@bp.route("/new", methods=["GET", "POST"])
@bp.route("/edit/<name>", methods=["GET", "POST"])
def tailor(name=None):
    db = get_db()

    if request.method == "POST":
        update_known_recipes(db, "tailoring", request)
        return redirect("/drmc/tailoring")

    recipes = get_recipes(db, "tailoring")
    player_recipes = []
    player_name = ""

    if name:
        player = get_known_recipes(db, "tailoring", name)
        player_name = player["name"]

        if player["recipes"]:
            player_recipes = [int(recipe) for recipe in player["recipes"].split(",")]

    return render_template(
        "new_profession.html",
        profession="tailoring",
        recipes=recipes,
        name=player_name,
        player_recipes=player_recipes,
    )
