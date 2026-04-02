def get_jobs_source():
    now = datetime.now()

    return [
        {
            "id": "1",
            "title": "Product Owner",
            "company": "Tech Corp",
            "url": "https://www.linkedin.com/jobs/view/1",
            "posted_at": (now - timedelta(hours=2)).isoformat()
        },
        {
            "id": "2",
            "title": "Analista de Dados",
            "company": "Data BR",
            "url": "https://www.linkedin.com/jobs/view/2",
            "posted_at": (now - timedelta(hours=3)).isoformat()
        },
        {
            "id": "3",
            "title": "Backend Developer Python",
            "company": "Startup BR",
            "url": "https://www.linkedin.com/jobs/view/3",
            "posted_at": (now - timedelta(hours=5)).isoformat()
        }
    ]