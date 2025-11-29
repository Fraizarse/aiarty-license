from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

# AppSumo endpoints - return exactly what they expect
@app.route('/api/appsumo/activate', methods=['POST', 'GET'])
def activate():
    return Response('{"message":"Success","redirect_url":"https://web-production-672cf.up.railway.app"}', status=200, mimetype='application/json')

@app.route('/api/appsumo/deactivate', methods=['POST', 'GET'])
def deactivate():
    return Response('{"message":"Success"}', status=200, mimetype='application/json')

@app.route('/api/appsumo/enhance_tier', methods=['POST', 'GET'])
def enhance_tier():
    return Response('{"message":"Success","redirect_url":"https://web-production-672cf.up.railway.app"}', status=200, mimetype='application/json')

@app.route('/api/appsumo/reduce_tier', methods=['POST', 'GET'])
def reduce_tier():
    return Response('{"message":"Success"}', status=200, mimetype='application/json')

@app.route('/api/redeem', methods=['POST'])
def redeem():
    data = request.json
    system = data.get('system', '').lower()
    keys = {"windows": "FAKWB-BZWSM-UWEX4-IYF3C", "mac": "FBGLM-HWG5O-FOWWK-JWRHC"}
    return Response(json.dumps({'success': True, 'license_key': keys.get(system, keys['windows'])}), mimetype='application/json')

@app.route('/health')
def health():
    return Response('{"status":"ok"}', mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
