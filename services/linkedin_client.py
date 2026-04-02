import os
import requests
from datetime import datetime, timedelta
import random

class LinkedInClient:
    """
    Integração preparada para API oficial do LinkedIn.
    Atualmente retorna mock estruturado (substituir por OAuth real).
    """

    def __init__(self):
        self.base_url = "https://api.linkedin.com/v2"
        self.token = os.getenv("LINKEDIN_TOKEN", "")

    def search_jobs(self, query: str):
        # MOCK profissional (substituir por API oficial depois)
        now = datetime.now()

        mock = [
            {
                "id": "1",
                "title": f"{query or 'Dev Python'} Backend",
                "company": "Tech Corp",
                "posted_at": (now - timedelta(hours=2)).isoformat()
            },
            {
                "id": "2",
                "title": "Engenheiro de Software",
                "company": "Startup BR",
                "posted_at": (now - timedelta(hours=10)).isoformat()
            },
            {
                "id": "3",
                "title": "Full Stack Developer",
                "company": "AI Labs",
                "posted_at": (now - timedelta(hours=26)).isoformat()
            }
        ]

        random.shuffle(mock)
        return mock