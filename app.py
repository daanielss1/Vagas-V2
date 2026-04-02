from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# -----------------------------
# DADOS MOCK (ou scraping futuro)
# -----------------------------
def get_jobs():
    now = datetime.now()

    return [
        {
            "id": 1,
            "title": "Product Owner",
            "company": "Tech Corp",
            "url": "https://example.com/1",
            "posted_at": (now - timedelta(hours=2)).isoformat()
        },
        {
            "id": 2,
            "title": "Backend Developer",
            "company": "Startup BR",
            "url": "https://example.com/2",
            "posted_at": (now - timedelta(hours=5)).isoformat()
        },
        {
            "id": 3,
            "title": "Analista de Dados",
            "company": "Data Corp",
            "url": "https://example.com/3",
            "posted_at": (now - timedelta(hours=10)).isoformat()
        },
        {
            "id": 4,
            "title": "Product Owner Senior",
            "company": "Global Tech",
            "url": "https://example.com/4",
            "posted_at": (now - timedelta(hours=20)).isoformat()
        },
        {
            "id": 5,
            "title": "DevOps Engineer",
            "company": "Cloud BR",
            "url": "https://example.com/5",
            "posted_at": (now - timedelta(hours=30)).isoformat()
        }
    ]


# -----------------------------
# FRONT
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# API PRINCIPAL (CORRIGIDA)
# -----------------------------
@app.route("/api/jobs")
def jobs():

    q = request.args.get("q", "").strip().lower()
    hours = int(request.args.get("hours", 24))

    limit_time = datetime.now() - timedelta(hours=hours)

    results = []

    for job in get_jobs():

        posted = datetime.fromisoformat(job["posted_at"])

        # 1. filtro de tempo (OBRIGATÓRIO)
        if posted < limit_time:
            continue

        # 2. filtro de busca (CORRETO)
        if q:
            title = job["title"].lower()
            company = job["company"].lower()

            if q not in title and q not in company:
                continue

        results.append(job)

    # mais recentes primeiro
    results.sort(key=lambda x: x["posted_at"], reverse=True)

    return jsonify(results)


# -----------------------------
# APLICAÇÕES
# -----------------------------
applied = []


@app.route("/api/apply", methods=["POST"])
def apply():
    job = request.json
    applied.append(job)
    return jsonify({"ok": True})


@app.route("/api/applied")
def get_applied():
    return jsonify(applied)


# -----------------------------
# RUN (RENDER COMPATÍVEL)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)