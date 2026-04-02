from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)


# -----------------------------
# BASE SIMULADA
# -----------------------------
def get_jobs_source():
    now = datetime.now()

    return [
        {
            "id": "1",
            "title": "Product Owner",
            "company": "Tech Corp",
            "posted_at": (now - timedelta(hours=2)).isoformat()
        },
        {
            "id": "2",
            "title": "Backend Developer Python",
            "company": "Startup BR",
            "posted_at": (now - timedelta(hours=4)).isoformat()
        },
        {
            "id": "3",
            "title": "Product Owner Senior",
            "company": "Global Systems",
            "posted_at": (now - timedelta(hours=6)).isoformat()
        },
        {
            "id": "4",
            "title": "DevOps Engineer",
            "company": "Cloud Infra",
            "posted_at": (now - timedelta(hours=10)).isoformat()
        },
        {
            "id": "5",
            "title": "Frontend React Developer",
            "company": "Digital Factory",
            "posted_at": (now - timedelta(hours=12)).isoformat()
        }
    ]


# -----------------------------
# FRONT
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# API DE BUSCA (CORRETA AGORA)
# -----------------------------
@app.route("/api/jobs")
def jobs():

    q = request.args.get("q", "").strip().lower()
    hours = int(request.args.get("hours", 24))

    # 🚨 REGRA 1: se não tem busca, NÃO retorna nada
    if not q:
        return jsonify([])

    source = get_jobs_source()

    limit_time = datetime.now() - timedelta(hours=hours)

    result = []

    for job in source:
        posted_time = datetime.fromisoformat(job["posted_at"])

        # filtro de tempo
        if posted_time < limit_time:
            continue

        title = job["title"].lower()
        company = job["company"].lower()

        # 🚨 REGRA 2: match EXATO / REAL (sem mistura)
        words = q.split()

        match = all(
            any(w in title or w in company for w in words)
        )

        if match:
            result.append(job)

    # ordenação
    result.sort(key=lambda x: x["posted_at"], reverse=True)

    return jsonify(result)


# -----------------------------
# APLICAÇÃO
# -----------------------------
applied = []


@app.route("/api/apply", methods=["POST"])
def apply():
    job = request.json

    if job not in applied:
        applied.append(job)

    return jsonify({"status": "ok"})


@app.route("/api/applied")
def get_applied():
    return jsonify(applied)


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)