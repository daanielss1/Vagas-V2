from flask import Flask, render_template, request, jsonify
from services.linkedin_client import LinkedInClient
from database.db import init_db, mark_applied, get_applied
from core.jobs import filter_jobs
import os

app = Flask(__name__)

# Inicializa banco
init_db()


# -------------------------
# FRONT
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# LISTAR VAGAS
# -------------------------
@app.route("/api/jobs")
def jobs():
    q = request.args.get("q", "")
    hours = int(request.args.get("hours", 24))

    client = LinkedInClient()

    jobs = client.search_jobs(q)

    applied = get_applied()
    applied_ids = [a["id"] for a in applied]

    filtered = filter_jobs(jobs, hours, applied_ids)

    return jsonify(filtered)


# -------------------------
# MARCAR COMO APLICADA
# -------------------------
@app.route("/api/apply", methods=["POST"])
def apply():
    job = request.json
    mark_applied(job)
    return jsonify({"status": "ok"})


# -------------------------
# LISTAR APLICADAS
# -------------------------
@app.route("/api/applied")
def applied():
    return jsonify(get_applied())


# -------------------------
# RENDER ENTRYPOINT (CRÍTICO)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)