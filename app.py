from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import os
import re

app = Flask(__name__)


# -----------------------------
# BASE SIMULADA
# -----------------------------
def get_jobs_source():
    now = datetime.now()

    return [
        {"id": "1", "title": "Product Owner", "company": "Tech Corp",
         "posted_at": (now - timedelta(hours=2)).isoformat()},

        {"id": "2", "title": "Analista de Dados", "company": "Data BR",
         "posted_at": (now - timedelta(hours=3)).isoformat()},

        {"id": "3", "title": "Backend Developer Python", "company": "Startup BR",
         "posted_at": (now - timedelta(hours=5)).isoformat()},

        {"id": "4", "title": "Analista de Sistemas", "company": "Global Systems",
         "posted_at": (now - timedelta(hours=10)).isoformat()},

        {"id": "5", "title": "Product Owner Senior", "company": "Tech Global",
         "posted_at": (now - timedelta(hours=12)).isoformat()},

        {"id": "6", "title": "DevOps Engineer AWS", "company": "Cloud Infra",
         "posted_at": (now - timedelta(hours=18)).isoformat()},
    ]


# -----------------------------
# FRONT
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# NORMALIZA TEXTO (IMPORTANTE)
# -----------------------------
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # remove símbolos tipo "+"
    text = re.sub(r'\s+', ' ', text)          # remove espaços duplicados
    return text.strip()


# -----------------------------
# API PRINCIPAL (CORRIGIDA)
# -----------------------------
@app.route("/api/jobs")
def jobs():

    q = request.args.get("q", "")
    hours = int(request.args.get("hours", 24))

    jobs = get_jobs_source()

    limit_time = datetime.now() - timedelta(hours=hours)

    # 🚨 SE NÃO TEM BUSCA → RETORNA LISTA VAZIA (COMO VOCÊ QUER)
    if not q.strip():
        return jsonify([])

    q = normalize(q)
    query_words = q.split()

    result = []

    for job in jobs:
        posted = datetime.fromisoformat(job["posted_at"])

        # 1. filtro de tempo CORRETO
        if posted < limit_time:
            continue

        title = normalize(job["title"])
        company = normalize(job["company"])

        # 2. MATCH FLEXÍVEL (SEM MATAR RESULTADOS)
        score = 0

        for word in query_words:
            if word in title:
                score += 3
            if word in company:
                score += 1

        # 3. regra simples: qualquer match entra
        if score > 0:
            job["score"] = score
            result.append(job)

    # 4. ordenação por relevância + tempo
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