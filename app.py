from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)


# -----------------------------
# BASE DE VAGAS (SIMULADO)
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
            "posted_at": (now - timedelta(hours=3)).isoformat()
        },
        {
            "id": "3",
            "title": "Product Owner Senior",
            "company": "Global Systems",
            "posted_at": (now - timedelta(hours=5)).isoformat()
        },
        {
            "id": "4",
            "title": "DevOps Engineer AWS",
            "company": "Cloud Infra",
            "posted_at": (now - timedelta(hours=8)).isoformat()
        },
        {
            "id": "5",
            "title": "Frontend React Developer",
            "company": "Digital Factory",
            "posted_at": (now - timedelta(hours=10)).isoformat()
        }
    ]


# -----------------------------
# FRONT
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# API DE BUSCA (CORRIGIDA DE VERDADE)
# -----------------------------
@app.route("/api/jobs")
def jobs():

    q = request.args.get("q", "").strip().lower()
    hours = int(request.args.get("hours", 24))

    jobs = get_jobs_source()

    limit_time = datetime.now() - timedelta(hours=hours)

    result = []

    for job in jobs:
        posted = datetime.fromisoformat(job["posted_at"])

        # filtro de tempo
        if posted < limit_time:
            continue

        # 🚨 REGRA NOVA: se NÃO tem busca, NÃO retorna nada
        if not q:
            return jsonify([])

        title = job["title"].lower()
        company = job["company"].lower()

        # 🔥 MATCH INTELIGENTE (SEM QUEBRAR)
        query_words = q.split()

        match_score = 0

        for word in query_words:
            if word in title:
                match_score += 2
            if word in company:
                match_score += 1

        # só entra se tiver QUALQUER relevância
        if match_score > 0:
            job["score"] = match_score
            result.append(job)

    # ordena por relevância + recência
    result.sort(key=lambda x: (x["score"], x["posted_at"]), reverse=True)

    return jsonify(result)


# -----------------------------
# APLICAÇÕES
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