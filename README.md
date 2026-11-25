# Namma Seva — ನಮ್ಮ ಸೇವೆ

**Kannada-first officer workflow demo** for processing income-certificate applications. The demo uses fictional applicants and is not affiliated with Karnataka government systems. It does not connect to Nadakacheri or any live government database.

## Problem and users
Frontline and extension-level revenue staff often need to inspect documents, coordinate field verification, write reports, and forward a case for a decision. A slow or fragmented workflow can create repeat visits, unclear status, and overdue cases. Namma Seva focuses on the officer's work queue, making urgency, next action, checklist and history visible in one phone-friendly workspace.

Primary users represented: Village Accountant / Revenue Inspector and reviewing caseworker. The prototype uses fictional localities around Bengaluru rural/urban examples.

## Workflow
1. **Document review (ದಾಖಲೆ ಪರಿಶೀಲನೆ):** review submitted facts and mark identity, address, income proof and family details checklist. Unchecked items are only prompts to inspect—not an eligibility finding.
2. **Field verification (ಕ್ಷೇತ್ರ ಪರಿಶೀಲನೆ):** add officer observations and proceed to report submission. In this demo, field observations are stored as officer notes.
3. **Decision review (ನಿರ್ಧಾರ):** review the application and report context, then manually approve, reject, or return it. Return/reject requires a written reason. The worker remains responsible for every decision.
4. **Audit-style history:** stage changes and officer remarks are added to the application's visible timeline.

The process is intentionally simplified. Actual routing, delegated powers, service-level deadlines, required evidence, and legal decision criteria must be validated with the local taluk and current official instructions before operational use.

## AI assistance and safeguards
- **Summary:** condenses only the application fields shown in the demo.
- **Checklist review:** highlights unchecked document items and suggests what should be inspected.
- **Report drafting:** drafts neutral Kannada text the officer can edit.
- **Human control:** AI does not calculate eligibility, infer fraud, or make approval/rejection decisions. Officer remarks and final action are manual.
- **Privacy:** do not enter real citizen data. The seed records are fictional. With `OPENAI_API_KEY` configured, the server sends the submitted demo fields to the configured AI API. Do not deploy with real data until a privacy/security review, authorization, retention, logging, and data minimization are implemented.

Without an API key, AI buttons use deterministic local demo templates. With an API key, the backend attempts an OpenAI Responses API call and falls back to local text if the request fails.

## How to measure impact
Run a small controlled pilot, comparing baseline and pilot cohorts by taluk/service. Track:
- Median and p90 receipt-to-decision turnaround.
- Officer handling minutes per case; report drafting time.
- Backlog size and age; overdue percentage.
- Returned cases and repeat visits attributable to unclear requests.
- Audit quality: reversals, appeal outcomes, and sample review for unsupported decisions.
- Usability: task completion time, errors, field-worker feedback, and low-connectivity recovery.

Speed alone is not a success: decision quality, accessibility, and fairness should not regress.

## Technical decisions
- **Frontend:** single responsive HTML/CSS/vanilla JavaScript file for a zero-build static prototype.
- **Storage:** local browser `localStorage` persists demo actions and checklist changes across refreshes. Reset Demo clears the saved state.
- **Optional server:** small Python standard-library HTTP server serves the UI and provides `/api/assist`; without it (e.g. static hosting), the UI's local mock AI remains functional.
- **AI:** optional server-side OpenAI Responses API call using environment variables; API key is never placed in frontend code. The AI request is limited to fictional demo fields. No production auth, database, access control, secure audit log, offline sync, or official integration exists.
- **Demo sign-in:** `officer / demo123`. This is a front-end demo gate, not real authentication; do not treat it as security or deploy with real personal data.
- **Interface:** Kannada-first copy, large click targets, responsive cards, explicit stage/status, and timeline history.

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

## Optional AI configuration
Set the key only in your server environment (never commit it):

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4.1-mini"
# Optional for compatible proxy/provider endpoint:
export OPENAI_API_URL="https://api.openai.com/v1/responses"
python server.py
```

## Deploy (Render)
1. Push this folder to a GitHub repository.
2. Create a new Render Web Service from the repo, or use the included `render.yaml` blueprint.
3. Build command: `pip install -r requirements.txt` (no external packages needed).
4. Start command: `python server.py`.
5. Set `OPENAI_API_KEY` in Render environment variables only if you want live AI; leave it unset for deterministic demo templates.
6. Verify `/` loads, demo login works, AI returns mock or AI mode, and workflow actions persist in the browser.

**Important:** public demo credentials are intentionally visible and the login gate is client-side. This is not production authentication. A submission deployment should use only fictional sample data. Production needs real authentication, server-side authorization, secure database storage, encryption, consent/retention controls, and tamper-resistant audit logging.

## Demo walkthrough
1. Log in with the demo credentials.
2. Dashboard: scan backlog, overdue and stage counts.
3. Search/filter an application and open it.
4. Use summary, checklist-gap, or report-draft AI assistance (mock unless server key configured).
5. Mark checklist items and add officer remarks; changes persist locally.
6. Move review → field verification → decision.
7. Approve/reject/return with a reason; inspect timeline.
8. Reset Demo to restore the original seeded dataset.

## Process references
- Tumkur District official income-certificate process: https://tumkur.nic.in/en/service/apply-for-income-certificate/
- Karnataka AJSK/Nadakacheri workflow reference PDF: https://www.statusin.in/uploads/20692-WorkFlow.pdf

References are used as process inspiration. This demo is not an authoritative statement that every taluk follows identical steps or that it is an official service portal.
