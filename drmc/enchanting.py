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
from drmc import scan_enchants, get_recipes, get_known_recipes, update_known_recipes

bp = Blueprint("enchant", __name__, url_prefix="/drmc/enchanting")


@bp.route("/", methods=["GET"])
def enchant():
    db = get_db()

    recipes = get_recipes(db, "enchanting")
    players = get_known_recipes(db, "enchanting")

    player_recipes = {}
    player_availability = {}

    for player in players:
        if player["recipes"]:
            player_recipes[player["name"]] = [
                int(recipe) for recipe in player["recipes"].split(",")
            ]

    return render_template(
        "profession.html",
        profession="enchanting",
        recipes=recipes,
        players=player_recipes,
        player_count=len(players) + 1,
    )


@bp.route("/new", methods=["GET", "POST"])
@bp.route("/edit/<name>", methods=["GET", "POST"])
def enchanter(name=None):
    db = get_db()

    if request.method == "POST":
        update_known_recipes(db, "enchanting", request)
        return redirect("/drmc/enchanting")

    recipes = get_recipes(db, "enchanting")
    player_recipes = []
    player_name = ""

    if name:
        player = get_known_recipes(db, "enchanting", name)
        player_name = player["name"]

        if player["recipes"]:
            player_recipes = [int(recipe) for recipe in player["recipes"].split(",")]

    return render_template(
        "new_profession.html",
        profession="enchanting",
        recipes=recipes,
        name=player_name,
        player_recipes=player_recipes,
    )


@bp.route("/rescan", methods=["GET"])
def rescan():
    scan_enchants()
    flash("Enchanter and enchant information updated", "positive")
    return redirect("/drmc/enchanting/")
