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
from drmc import get_recipes, get_known_recipes

bp = Blueprint("alchemy", __name__, url_prefix="/drmc/alchemy")


@bp.route("/", methods=["GET"])
def alchemy():
    db = get_db()
    recipes = get_recipes(db, "alchemy")
    players = get_known_recipes(db, "alchemy")

    player_recipes = {}
    player_availability = {}

    for player in players:
        if player["recipes"]:
            player_recipes[player["name"]] = [
                int(recipe) for recipe in player["recipes"].split(",")
            ]

    return render_template(
        "profession.html",
        profession="alchemy",
        recipes=recipes,
        players=player_recipes,
        player_count=len(players) + 1,
    )


@bp.route("/new", methods=["GET", "POST"])
@bp.route("/edit/<name>", methods=["GET", "POST"])
def alchemist(name=None):
    db = get_db()

    if request.method == "POST":
        update_known_recipes(db, "alchemy", request)
        return redirect("/drmc/alchemy")

    recipes = get_recipes(db, "alchemy")
    player_recipes = []
    player_name = ""

    if name:
        player = get_known_recipes(db, "alchemy", name)
        player_name = player["name"]

        if player["recipes"]:
            player_recipes = [int(recipe) for recipe in player["recipes"].split(",")]

    return render_template(
        "new_profession.html",
        profession="alchemy",
        recipes=recipes,
        name=player_name,
        player_recipes=player_recipes,
    )
