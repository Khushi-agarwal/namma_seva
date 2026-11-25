# Namma Seva — ನಮ್ಮ ಸೇವೆ

**Kannada-first officer workflow demo** for processing income-certificate applications. The demo uses fictional applicants and is not affiliated with Karnataka government systems. It does not connect to Nadakacheri or any live government database.

## Run locally
Python 3.10+ recommended. No third-party dependencies required.


```bash
cd namma_seva
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python server.py
```
Open `http://localhost:5000` and log in using:
- Username: `officer`
- Password: `demo123`

You can also open `index.html` directly; local mock AI and browser-local state still work, but the server-backed AI route is unavailable.

**Important:** public demo credentials are intentionally visible and the login gate is client-side. This is not production authentication. 
## Demo walkthrough
1. Log in with the demo credentials.
2. Dashboard: scan backlog, overdue and stage counts.
3. Search/filter an application and open it.
4. Use summary, checklist-gap, or report-draft AI assistance (mock unless server key configured).
5. Mark checklist items and add officer remarks; changes persist locally.
6. Move review → field verification → decision.
7. Approve/reject/return with a reason; inspect timeline.
8. Reset Demo to restore the original seeded dataset.

