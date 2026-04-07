import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_DIR = Path("data")
KRI_PATH = DATA_DIR / "kriteria.csv"
ALT_PATH = DATA_DIR / "alternatif.csv"

DATA_DIR.mkdir(exist_ok=True)

def load_csv(path):
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@app.route("/")
def index():
    kriteria = load_csv(KRI_PATH)
    alternatif = load_csv(ALT_PATH)

    return render_template(
        "index.html",
        kriteria=kriteria.to_html(index=False) if not kriteria.empty else "<p>Belum ada data</p>",
        alternatif=alternatif.to_html(index=False) if not alternatif.empty else "<p>Belum ada data</p>",
        info_kriteria=info_data(kriteria),
        info_alternatif=info_data(alternatif),
    )

@app.route("/upload", methods=["POST"])
def upload():
    if "kriteria" in request.files:
        request.files["kriteria"].save(KRI_PATH)
    if "alternatif" in request.files:
        request.files["alternatif"].save(ALT_PATH)
    return redirect(url_for("index"))

def info_data(df):
    return {
        "baris": df.shape[0],
        "kolom": df.shape[1]
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)