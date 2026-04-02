from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# -----------------------------
# BASE DE VAGAS (SIMULANDO LINKEDIN)
# -----------------------------
def get_jobs_source():
    now = datetime.now()

    return [
        {
            "id": "1",
            "title": "Backend Python Developer",
            "company": "Tech Corp",
            "posted_at": (now - timedelta(hours=2)).isoformat()
        },
        {
            "id": "2",
            "title": "Full Stack Developer React Python",
            "company": "Startup BR",
            "posted_at": (now - timedelta(hours=5)).isoformat()
        },
        {
            "id": "3",
            "title": "DevOps Engineer AWS",
            "company": "Cloud Systems",
            "posted_at": (now - timedelta(hours=8)).isoformat()
        },
        {
            "id": "4",
            "title": "Data Engineer Python",
            "company": "AI Labs",
            "posted_at": (now - timedelta(hours=12)).isoformat()
        },
        {
            "id": "5",
            "title": "Software Engineer Java Backend",
            "company": "Global Tech",
            "posted_at": (now - timedelta(hours=18)).isoformat()
        },
        {
            "id": "6",
            "title": "Cloud Architect",
            "company": "Infra Global",
            "posted_at": (now - timedelta(hours=22)).isoformat()
        },
        {
            "id": "7",
            "title": "Backend Engineer Node.js",
            "company": "Digital Factory",
            "posted_at": (now - timedelta(hours=23)).isoformat()
        }
    ]


# -----------------------------
# FRONT
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# API PRINCIPAL (CORRIGIDA DE VERDADE)
# -----------------------------
@app.route("/api/jobs")
def jobs():

    q = request.args.get("q", "").strip().lower()
    hours = int(request.args.get("hours", 24))

    source = get_jobs_source()

    limit_time = datetime.now() - timedelta(hours=hours)

    result = []

    for job in source:
        posted_time = datetime.fromisoformat(job["posted_at"])

        # 1. FILTRO DE TEMPO (12h / 24h)
        if posted_time < limit_time:
            continue

        # 2. FILTRO DE BUSCA (SEM MATAR RESULTADOS)
        if q:
            title = job["title"].lower()
            company = job["company"].lower()

            # match mais flexível (EVITA SOBRAR 1 ITEM)
            if q not in title and q not in company:
                continue

        result.append(job)

    # 3. ORDENAÇÃO (MAIS RECENTE PRIMEIRO)
    result.sort(key=lambda x: x["posted_at"], reverse=True)

    return jsonify(result)


# -----------------------------
# APLICAÇÃO (SALVA VAGAS)
# -----------------------------
applied = []


@app.route("/api/apply", methods=["POST"])
def apply():
    job = request.json

    # evita duplicar
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