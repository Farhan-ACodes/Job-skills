# AI Job Search Tool

A Python job search helper and Flask website that matches skills and locations against public job APIs. It reports application links and source-reported salaries where available, ranks likely early-career and high-demand-field matches, and provides heuristic learning roadmaps, career-path ideas, courses, and mentorship communities.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run the website

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. The website uses the same public job sources as the command-line tool. Remotive and Arbeitnow are enabled without credentials; USAJOBS and Adzuna need the environment variables described below. Flask's built-in server is for local development, not production hosting.

## Examples

```powershell
python ai_job_tool.py --skills "Python,data analysis" --locations "India,Canada,UK"
python ai_job_tool.py --skills "Python,cloud" --locations "US" --portals "remotive,arbeitnow,usajobs,adzuna" --experience Entry --job-type Full-time --json
python ai_job_tool.py --skills "Python,AI" --locations "Dubai" --migration-project "portable assistant migration"
```

`--job-type` and `--experience` can each be supplied more than once. Supported job types are Full-time, Part-time, Contract, and Internship; experience levels are Entry, Mid, and Senior. `--json` emits job records, roadmaps, provider errors, portal counts, and career guidance.

## Job sources and configuration

- Remotive and Arbeitnow use their public job-board APIs and are enabled by default.
- USAJOBS requires a registered `USAJOBS_API_KEY` and `USAJOBS_USER_AGENT` (the email address supplied during registration).
- Adzuna requires `ADZUNA_APP_ID` and `ADZUNA_APP_KEY`. The country-specific API is selected for India, US, Canada, and UK locations.

Set credentials in the environment; do not put secrets in this project. LinkedIn and Indeed are not scraped because their pages are access-controlled and automated scraping may violate their terms. This version does not query India's government job portal or Gulf-country portals directly; add a provider for an official API or approved feed rather than relying on unauthorized scraping. Provider failures, including missing optional credentials, are displayed while successful providers still return results.

## Matching and guidance limitations

This tool is a search aid, not a job-market database. Portals may return partial or stale results, and location filtering is literal text matching (worldwide remote listings are accepted for any selected location). Salary is displayed only when supplied by a source; no salary estimate is fabricated. Startup/early-career highlighting is based on wording in the listing, not independently verified company hiring history. Technology-field labels, rankings, career paths, and learning roadmaps are heuristic and not labor-market forecasts or guarantees. Adzuna is currently queried only for India, US, Canada, and UK locations. If supplied, migration-project details are included in search requests to the selected job providers and used to rank relevant listings; they are not sent to an AI service.

## Tests

```powershell
python -m unittest -v
```
