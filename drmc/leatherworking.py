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

bp = Blueprint("leatherworking", __name__, url_prefix="/drmc/leatherworking")


@bp.route("/", methods=["GET"])
def leatherworking():
    db = get_db()

    recipes = get_recipes(db, "leatherworking")
    players = get_known_recipes(db, "leatherworking")

    player_recipes = {}
    player_availability = {}

    for player in players:
        if player["recipes"]:
            player_recipes[player["name"]] = [
                int(recipe) for recipe in player["recipes"].split(",")
            ]

    return render_template(
        "profession.html",
        profession="leatherworking",
        recipes=recipes,
        players=player_recipes,
        player_count=len(players) + 1,
    )


@bp.route("/new", methods=["GET", "POST"])
@bp.route("/edit/<name>", methods=["GET", "POST"])
def chef(name=None):
    db = get_db()

    if request.method == "POST":
        update_known_recipes(db, "leatherworking", request)
        return redirect("/drmc/leatherworking")

    recipes = get_recipes(db, "leatherworking")
    player_recipes = []
    player_name = ""

    if name:
        player = get_known_recipes(db, "leatherworking", name)
        player_name = player["name"]

        if player["recipes"]:
            player_recipes = [int(recipe) for recipe in player["recipes"].split(",")]

    return render_template(
        "new_profession.html",
        profession="leatherworking",
        recipes=recipes,
        name=player_name,
        player_recipes=player_recipes,
    )
