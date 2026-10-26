"""Flask website for the AI Job Search Tool."""

import html
import re
from urllib.parse import urlsplit

from flask import Flask, render_template, request

import ai_job_tool

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

PORTALS = tuple(ai_job_tool.PROVIDERS)
JOB_TYPES = ("Full-time", "Part-time", "Contract", "Internship")
EXPERIENCE_LEVELS = ("Entry", "Mid", "Senior")


def _safe_job_url(value: str) -> str:
    """Only render provider-supplied links that can safely be opened as websites."""
    try:
        parsed = urlsplit(value)
        return value if parsed.scheme in {"http", "https"} and parsed.netloc else ""
    except ValueError:
        return ""


def _plain_text(value: str) -> str:
    text = html.unescape(re.sub(r"<[^>]*>", " ", value))
    return re.sub(r"\s+", " ", text).strip()


@app.route("/", methods=["GET", "POST"])
def index():
    form = {
        "skills": request.form.get("skills", ""),
        "locations": request.form.get("locations", ""),
        "migration_project": request.form.get("migration_project", ""),
        "portals": request.form.getlist("portals") if request.method == "POST" else ["remotive", "arbeitnow"],
        "job_types": request.form.getlist("job_types"),
        "experiences": request.form.getlist("experiences"),
    }
    error = ""
    jobs = []
    provider_errors = {}
    guidance = None
    searched = request.method == "POST"

    if searched:
        skills = ai_job_tool._csv_values(form["skills"])
        locations = ai_job_tool._csv_values(form["locations"])
        invalid_portals = [portal for portal in form["portals"] if portal not in PORTALS]
        invalid_types = [value for value in form["job_types"] if value not in JOB_TYPES]
        invalid_experience = [value for value in form["experiences"] if value not in EXPERIENCE_LEVELS]

        if not skills:
            error = "Add at least one skill or job keyword to start your search."
        elif invalid_portals or not form["portals"]:
            error = "Select at least one valid job source."
        elif invalid_types or invalid_experience:
            error = "One of the selected job filters is not supported. Please choose from the listed options."
        else:
            raw_jobs, provider_errors = ai_job_tool.search_jobs(
                skills=skills,
                locations=locations,
                portals=form["portals"],
                job_types=form["job_types"],
                experiences=form["experiences"],
                migration_project=form["migration_project"].strip()[:300],
            )
            jobs = [ai_job_tool._job_record(job, skills) for job in raw_jobs]
            for job in jobs:
                job["url"] = _safe_job_url(job["url"])
                job["description"] = _plain_text(job["description"])
            guidance = ai_job_tool._career_guidance(skills, raw_jobs)

    return render_template(
        "index.html",
        form=form,
        error=error,
        jobs=jobs,
        provider_errors=provider_errors,
        guidance=guidance,
        searched=searched,
        portals=PORTALS,
        portal_labels=ai_job_tool.PORTAL_LABELS,
        job_types=JOB_TYPES,
        experience_levels=EXPERIENCE_LEVELS,
        locations=ai_job_tool._csv_values(form["locations"]),
    ), (400 if error else 200)


if __name__ == "__main__":
    app.run(debug=False)
