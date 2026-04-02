from datetime import datetime, timedelta
import random

class LinkedInClient:
    def search_jobs(self, query: str):
        now = datetime.now()

        base = [
            {
                "id": "1",
                "title": f"{query or 'Python Dev'} Backend Developer",
                "company": "Tech Corp",
                "posted_at": (now - timedelta(hours=2)).isoformat()
            },
            {
                "id": "2",
                "title": "Full Stack Engineer",
                "company": "Startup BR",
                "posted_at": (now - timedelta(hours=10)).isoformat()
            },
            {
                "id": "3",
                "title": "Cloud Engineer",
                "company": "AI Labs",
                "posted_at": (now - timedelta(hours=20)).isoformat()
            },
            {
                "id": "4",
                "title": "DevOps Engineer",
                "company": "Infra Global",
                "posted_at": (now - timedelta(hours=30)).isoformat()
            }
        ]

        # filtro simples por texto (IMPORTANTE)
        if query:
            base = [
                j for j in base
                if query.lower() in j["title"].lower()
                or query.lower() in j["company"].lower()
            ]

        return base