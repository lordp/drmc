from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests

WOWHEAD_LINK = r"https://www.wowhead.com/classic/spell=([\d]+)/([a-z\-]+)"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="/drmc/static/",
        static_url_path="/drmc/static",
    )
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "drmc.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/drmc/", methods=["GET"])
    def index():
        return render_template("index.html")
        # return redirect("/drmc/bank/")

    from . import (
        db,
        bank,
        enchanting,
        alchemy,
        blacksmithing,
        engineering,
        tailoring,
        cooking,
        availability,
        leatherworking,
    )

    db.init_app(app)
    app.register_blueprint(bank.bp)
    app.register_blueprint(enchanting.bp)
    app.register_blueprint(alchemy.bp)
    app.register_blueprint(blacksmithing.bp)
    app.register_blueprint(engineering.bp)
    app.register_blueprint(tailoring.bp)
    app.register_blueprint(cooking.bp)
    app.register_blueprint(leatherworking.bp)
    app.register_blueprint(availability.bp)

    app.config["professions"] = {
        "Alchemy": "alchemy.alchemy",
        "Blacksmithing": "blacksmith.blacksmithing",
        "Cooking": "cook.cooking",
        "Enchanting": "enchant.enchant",
        "Engineering": "engineer.engineering",
        "Leatherworking": "leatherworking.leatherworking",
        "Tailoring": "tailor.tailoring",
    }

    @app.template_filter("count_colour")
    def count_colour(count):
        return "green" if count > 0 else "red"

    def is_active(url, path):
        return " active" if path in url else ""

    app.jinja_env.globals.update(is_active=is_active)

    return app


def get_recipes(db, profession):
    return db.execute(
        "SELECT * FROM recipes WHERE profession = ? ORDER BY name", (profession,)
    ).fetchall()


def get_known_recipes(db, profession, player=None):
    stmt = """
        SELECT p.name, GROUP_CONCAT(DISTINCT r.id) AS recipes, GROUP_CONCAT(DISTINCT pa.availability) AS availability
        FROM players AS p 
        LEFT JOIN player_recipes AS pr ON pr.player_id = p.id 
        LEFT JOIN recipes AS r ON pr.recipe_id = r.id AND r.profession = ?
        LEFT JOIN player_availability AS pa ON pa.player_id = p.id
    """

    if player:
        stmt += " WHERE LOWER(p.name) = ?"

    stmt += " GROUP BY p.id ORDER BY p.name"

    if player:
        return db.execute(stmt, (profession, player)).fetchone()
    else:
        return db.execute(stmt, (profession,)).fetchall()


def update_known_recipes(db, profession, request):
    name = request.form.get("name")
    recipes = request.form.getlist("recipe")
    new_recipes = request.form.get("new_recipes")

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

    # check new recipe links and add or discard them
    new_recipe_ids = []
    for recipe_link in re.split("\n|\r\n", new_recipes):
        recipe_info = re.findall(WOWHEAD_LINK, recipe_link)
        if len(recipe_info) == 1:
            new_recipe_ids.append(
                {"id": int(recipe_info[0][0]), "name": recipe_info[0][1]}
            )
            recipes.append(int(recipe_info[0][0]))

    # add any new recipes
    if len(new_recipe_ids) > 0:
        for new_recipe in new_recipe_ids:
            db.execute(
                "INSERT INTO recipes (id, name, profession) VALUES (?, ?, ?) ON CONFLICT DO NOTHING",
                (
                    new_recipe["id"],
                    new_recipe["name"],
                    profession,
                ),
            )

    # remove existing player recipe info
    db.execute(
        """
            DELETE FROM player_recipes
            WHERE ROWID IN (
                SELECT pr.ROWID FROM player_recipes AS pr
                INNER JOIN recipes AS r ON r.id = pr.recipe_id 
                WHERE pr.player_id = ? AND r.profession = ?
            )
            """,
        (
            player_id,
            profession,
        ),
    )

    # insert recipes
    for recipe_id in recipes:
        db.execute(
            "INSERT INTO player_recipes (player_id, recipe_id) VALUES (?, ?)",
            (player_id, recipe_id),
        )

    db.commit()

    flash("New recipes added", "positive")


def adjust_alt_name(alt):
    return alt.split("-")[0]


def item_scaffold(item_link):
    item = {
        "item_id": re.sub(r"Hitem:([0-9]+).*", r"\1", item_link.split("|")[2]),
        "name": re.sub(r"h\[([^\]]+)]", r"\1", item_link.split("|")[3]),
    }

    return item


def allowed_file(file):
    if file.filename != "GBankClassic.lua":
        return False

    first_line = file.readline()
    second_line = file.readline().strip()
    if second_line == b"GBankClassicDB = {":
        file.seek(0)
        return True

    return False


def process_upload(file):
    # save the uploaded file
    filename = secure_filename(file.filename)
    file.save(os.path.join("/tmp", filename))

    # convert from lua to json
    cmd = "/usr/bin/lua convert.lua"
    rv = os.system(cmd)

    skipped_alts = []

    # process was successful
    if rv == 0:
        with open("/tmp/GBankClassic.json") as infile:
            data = json.load(infile)

        conn = db.get_db()

        # remove existing data - clean up old alts/items
        conn.execute("DELETE FROM alts")
        conn.execute("DELETE FROM items")
        conn.commit()

        bank_alts = data["faction"]["Alliance"]["The Devils Rejects"]["alts"]
        valid_alts = data["faction"]["Alliance"]["The Devils Rejects"]["roster"]["alts"]
        for alt in bank_alts:
            if alt in valid_alts:
                items = {}

                # put the update timestamp into ISO format
                updated_at = datetime.fromtimestamp(bank_alts[alt]["version"])

                # get the current timestamp for this alt
                current_timestamp = conn.execute(
                    "SELECT updated_at FROM alts WHERE name = ?",
                    (adjust_alt_name(alt),),
                ).fetchone()

                # and make sure we're not uploading old data
                if current_timestamp and current_timestamp["updated_at"] >= updated_at:
                    skipped_alts.append(adjust_alt_name(alt))
                    continue

                # update time stamp for this alt
                conn.execute(
                    "INSERT INTO alts (name, updated_at) VALUES (?, ?) ON CONFLICT (name) DO UPDATE SET updated_at = ?",
                    (
                        adjust_alt_name(alt),
                        updated_at.isoformat(),
                        updated_at.isoformat(),
                    ),
                )
                conn.commit()

                alt_id = conn.execute(
                    "SELECT id FROM alts WHERE name = ?", (adjust_alt_name(alt),)
                ).fetchone()

                # catch alts with no bank or bags defined
                if "bank" not in bank_alts[alt]:
                    bank_alts[alt]["bank"] = {"items": []}

                if "bags" not in bank_alts[alt]:
                    bank_alts[alt]["bags"] = {"items": []}

                # consolodate bank and bag items
                for item in list(bank_alts[alt]["bags"]["items"]) + list(
                    bank_alts[alt]["bank"]["items"]
                ):
                    item_info = item_scaffold(item["Link"])
                    if item_info["item_id"] not in items:
                        items[item_info["item_id"]] = {
                            "name": item_info["name"],
                            "count": item["Count"],
                        }
                    else:
                        items[item_info["item_id"]]["count"] += item["Count"]

                # insert or update item counts
                for item_id, item_info in items.items():
                    # do we already have this item/alt combo recorded
                    db_item = conn.execute(
                        "SELECT * FROM items WHERE alt_id = ? AND item_id = ?",
                        (alt_id["id"], item_id),
                    ).fetchone()

                    if db_item:
                        # update counts
                        conn.execute(
                            "UPDATE items SET item_count = ? WHERE alt_id = ? AND item_id = ?",
                            (
                                item_info["count"],
                                alt_id["id"],
                                item_id,
                            ),
                        )
                    else:
                        # insert new item record
                        conn.execute(
                            "INSERT INTO items (alt_id, item_id, item_name, item_count) VALUES (?, ?, ?, ?)",
                            (
                                alt_id["id"],
                                item_id,
                                item_info["name"],
                                item_info["count"],
                            ),
                        )

                    conn.commit()

    return skipped_alts


def scan_enchants():
    # scan the google sheet and pull out relevant information
    html = requests.get(
        "https://docs.google.com/spreadsheets/d/17gZHvHm2fLeohxPYziaH6zYi5eCuET5iRZOK7KxQkB4/edit?gid=1891779207#gid=1891779207"
    ).text

    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")

    header = True
    players = []
    group_name_swap = {
        "Back": "Cloak",
        "Wrist": "Bracer",
        "Feet": "Boots",
        "Hands": "Gloves",
    }

    current_group = ""
    current_enchant = ""
    for row_idx, row in enumerate(tables[0].find_all("tr")):
        if row_idx == 0 or row_idx > 65:
            continue
        for col_idx, td in enumerate(row.find_all("td")):
            if row_idx == 1 and col_idx >= 2 and td.text:
                players.append({"name": td.text, "enchants": []})

            if row_idx > 2:
                if col_idx == 0:
                    if td["class"][0] == "s4":
                        current_group = td.text
                    else:
                        current_enchant = td.text

                if col_idx > 1 and td.text == "Yes":
                    players[col_idx - 2]["enchants"].append(
                        current_group + "|" + current_enchant
                    )

    conn = db.get_db()
    current_players = [
        row["name"] for row in conn.execute("SELECT name FROM players").fetchall()
    ]

    for player in players:
        if not player["name"] in current_players:
            # save the new player
            conn.execute("INSERT INTO players (name) VALUES (?)", (player["name"],))
            conn.commit()

        # get the player info
        player_id = conn.execute(
            "SELECT id FROM players WHERE name = ?", (player["name"],)
        ).fetchone()["id"]

        # assign known enchants to this player
        for enchant in player["enchants"]:
            # split group and enchant out
            group_name, enchant_name = enchant.split("|")
            if group_name in group_name_swap:
                group_name = group_name_swap[group_name]

            # get the enchant info
            enchant_id = conn.execute(
                "SELECT id FROM recipes WHERE name = ? AND group_name = ? AND profession = 'enchanting'",
                (
                    enchant_name,
                    group_name,
                ),
            ).fetchone()["id"]

            conn.execute(
                "INSERT OR IGNORE INTO player_recipes (player_id, recipe_id) VALUES (?, ?)",
                (player_id, enchant_id),
            )
            conn.commit()
