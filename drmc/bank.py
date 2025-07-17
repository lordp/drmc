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
from drmc import allowed_file, process_upload


bp = Blueprint("bank", __name__, url_prefix="/drmc/bank")


@bp.route("/", methods=["GET"])
def bank():
    bank_items = {}

    db = get_db()
    alts = db.execute("SELECT * FROM alts ORDER BY name").fetchall()
    items = db.execute("SELECT * FROM items ORDER BY item_name, alt_id").fetchall()

    for item in items:
        if item["item_id"] not in bank_items:
            bank_items[item["item_id"]] = {"name": item["item_name"], "counts": {}}
            for alt in alts:
                bank_items[item["item_id"]]["counts"][alt["id"]] = 0

        bank_items[item["item_id"]]["counts"][item["alt_id"]] = item["item_count"]

    return render_template("bank.html", alts=alts, items=bank_items)


@bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Bank file not included", "negative")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("Bank filename missing", "negative")
            return redirect(request.url)

        if file and allowed_file(file):
            skipped_alts = process_upload(file)

            flash("Bank data uploaded successfully", "positive")
            if len(skipped_alts) > 0:
                flash(
                    "Bank alts with old data skipped: " + ", ".join(skipped_alts),
                    "blue",
                )
            return redirect("/drmc/bank/")
        else:
            flash("Bank data file type is incorrect or malformed", "negative")

    return render_template("upload.html")
