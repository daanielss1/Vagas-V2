from datetime import datetime, timedelta

def filter_jobs(jobs, hours, applied_ids):
    limit = datetime.now() - timedelta(hours=hours)

    result = []

    for job in jobs:
        posted = datetime.fromisoformat(job["posted_at"])

        # regra: só mostra até 24h OU se já aplicada
        if posted >= limit or job["id"] in applied_ids:
            result.append(job)

    return sorted(result, key=lambda x: x["posted_at"], reverse=True)