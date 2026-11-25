"""Namma Seva demo server. Standard-library only; never use with real citizen data."""
import os, json, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        data = (ROOT / 'index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != '/api/assist':
            self.send_error(404)
            return
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
        except Exception:
            self.send_json(400, {'error': 'Invalid JSON body'})
            return
        case = payload.get('application', {})
        kind = payload.get('type', 'summary')
        stage = payload.get('stage', 'review')
        missing = [d.get('name', 'document') for d in case.get('documents', []) if not d.get('checked')]
        fallback = {
            'summary': f"ಅರ್ಜಿಯ ಸಾರಾಂಶ: {case.get('service','')} | ಕುಟುಂಬ: {case.get('familySize','')} | ಘೋಷಿತ ಆದಾಯ: {case.get('declaredIncome','')} | ಉದ್ದೇಶ: {case.get('purpose','')}. ಈ ಮಾಹಿತಿ ಅರ್ಜಿಯಲ್ಲಿರುವುದಷ್ಟೇ; ಮೂಲ ದಾಖಲೆಗಳನ್ನು ಅಧಿಕಾರಿಯೇ ಪರಿಶೀಲಿಸಬೇಕು.",
            'check': ('ದಾಖಲೆ ಪರಿಶೀಲನೆ ಸೂಚನೆ: ಪರಿಶೀಲಿಸದ checklist ಅಂಶಗಳು — ' + ', '.join(missing) + '. ಇದು ಕೇವಲ checklist ಸೂಚನೆ; ದಾಖಲೆಗಳ ನಿಜಾಸ್ತಿ/ಅರ್ಹತೆ ಕುರಿತು ತೀರ್ಮಾನವಲ್ಲ.') if missing else 'Checklist ನಲ್ಲಿ ಎಲ್ಲ ದಾಖಲೆಗಳನ್ನು ಗುರುತಿಸಲಾಗಿದೆ. ಮೂಲ ದಾಖಲೆಗಳ ನಿಜಾಸ್ತಿ ಮತ್ತು ಹೊಂದಾಣಿಕೆಯನ್ನು ಅಧಿಕಾರಿಯೇ ಪರಿಶೀಲಿಸಬೇಕು.',
            'draft': f"ವರದಿ ಕರಡು: {case.get('service','')} ಅರ್ಜಿಯ ಪ್ರಾಥಮಿಕ ಪರಿಶೀಲನೆಗೆ ಸಂಬಂಧಿಸಿದ ವಿವರಗಳನ್ನು ದಾಖಲಿಸಲಾಗಿದೆ. ಘೋಷಿತ ಕುಟುಂಬ ಆದಾಯ: {case.get('declaredIncome','')}; ಕುಟುಂಬ ಸದಸ್ಯರು: {case.get('familySize','')}. {('Checklist ನಲ್ಲಿ ಕೆಲವು ಅಂಶಗಳು ಬಾಕಿ ಇವೆ: '+', '.join(missing)+'.') if missing else 'Checklist ಪೂರ್ಣವಾಗಿದೆ.'} ಕ್ಷೇತ್ರದ ವಾಸ್ತವಾಂಶಗಳು ಮತ್ತು ಸಾಕ್ಷ್ಯವನ್ನು ಅಧಿಕಾರಿ ಸೇರಿಸಿ ಪರಿಶೀಲಿಸಿದ ನಂತರವೇ ಮುಂದಿನ ಕ್ರಮ ಕೈಗೊಳ್ಳಬೇಕು.",
        }
        fallback_text = fallback.get(kind, fallback['summary'])
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            self.send_json(200, {'text': fallback_text, 'mode': 'local-demo'})
            return
        task = {'summary':'Summarize the submitted application facts neutrally in Kannada, without inference.', 'check':'Explain unchecked checklist items in Kannada. Do not infer eligibility or fraud.', 'draft':'Draft a neutral editable Kannada officer report based only on these provided fields. Clearly identify missing evidence and avoid making decisions.'}.get(kind, 'Assist the officer neutrally in Kannada.')
        prompt = f"{task}\nWorkflow stage: {stage}\nData (fictional demo): {json.dumps(case, ensure_ascii=False)}\nRules: No eligibility score. Do not approve/reject. Do not invent facts. State limitations. Return concise Kannada text."
        endpoint = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/responses')
        model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
        body = json.dumps({'model': model, 'input': prompt, 'max_output_tokens': 400}).encode('utf-8')
        req = urllib.request.Request(endpoint, data=body, headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                result = json.loads(response.read())
            text = ''.join(part.get('text','') for item in result.get('output',[]) for part in item.get('content',[]) if part.get('type') == 'output_text').strip()
            self.send_json(200, {'text': text or fallback_text, 'mode': 'ai'})
        except Exception:
            self.send_json(200, {'text': fallback_text, 'mode': 'local-fallback'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    print(f'Namma Seva demo server listening on http://0.0.0.0:{port}')
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
