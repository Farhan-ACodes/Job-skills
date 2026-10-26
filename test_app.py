import unittest
from unittest.mock import patch

import app as web_app
import ai_job_tool


class JobSearchWebsiteTests(unittest.TestCase):
    def setUp(self):
        web_app.app.config["TESTING"] = True
        self.client = web_app.app.test_client()

    def test_home_page_shows_search_form_and_job_sources(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Build your job search", response.data)
        self.assertIn(b"Remotive", response.data)
        self.assertNotIn(b"Tech Corp", response.data)

    @patch.object(web_app.ai_job_tool, "search_jobs")
    def test_search_uses_selected_filters_and_renders_real_results(self, search_jobs):
        job = ai_job_tool.Job(
            "Python Developer",
            "Example Co",
            "Remote",
            "https://jobs.example.test/python",
            "remotive",
            description="<p>Build <strong>Python</strong> services &amp; tools.</p>",
        )
        search_jobs.return_value = ([job], {})

        response = self.client.post(
            "/",
            data={
                "skills": "Python, SQL",
                "locations": "Canada",
                "portals": ["remotive"],
                "job_types": ["Full-time"],
                "experiences": ["Entry"],
                "migration_project": "portable assistant",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Example Co", response.data)
        self.assertIn(b"https://jobs.example.test/python", response.data)
        self.assertIn(b"Build Python services &amp; tools.", response.data)
        self.assertNotIn(b"<strong>Python</strong>", response.data)
        search_jobs.assert_called_once_with(
            skills=["Python", "SQL"],
            locations=["Canada"],
            portals=["remotive"],
            job_types=["Full-time"],
            experiences=["Entry"],
            migration_project="portable assistant",
        )

    @patch.object(web_app.ai_job_tool, "search_jobs")
    def test_missing_skills_are_reported_without_searching(self, search_jobs):
        response = self.client.post("/", data={"portals": ["remotive"]})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Add at least one skill", response.data)
        search_jobs.assert_not_called()

    @patch.object(web_app.ai_job_tool, "search_jobs")
    def test_untrusted_job_url_is_not_rendered_as_an_apply_link(self, search_jobs):
        job = ai_job_tool.Job(
            "Python Developer",
            "Example Co",
            "Remote",
            "javascript:alert(1)",
            "remotive",
        )
        search_jobs.return_value = ([job], {})

        response = self.client.post(
            "/",
            data={"skills": "Python", "portals": ["remotive"]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Python Developer", response.data)
        self.assertNotIn(b"javascript:alert(1)", response.data)
        self.assertNotIn(b"View listing", response.data)


if __name__ == "__main__":
    unittest.main()
