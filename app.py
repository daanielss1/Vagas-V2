from flask import Flask, render_template, request, jsonify
from services.linkedin_client import LinkedInClient
from database.db import init_db, mark_applied, get_applied
from core.jobs import filter_jobs

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return render_template("index.html")


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


@app.route("/api/apply", methods=["POST"])
def apply():
    job = request.json
    mark_applied(job)
    return {"status": "ok"}


@app.route("/api/applied")
def applied():
    return jsonify(get_applied())


if __name__ == "__main__":
    app.run(debug=True)