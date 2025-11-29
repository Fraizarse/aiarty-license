"""
Aiarty License Server
Compatible with AppSumo Licensing API v2
"""

from flask import Flask, request, jsonify, send_file, Response
import json

app = Flask(__name__)

RAILWAY_URL = "https://web-production-672cf.up.railway.app"

LICENSE_KEYS = {
    "windows": "FAKWB-BZWSM-UWEX4-IYF3C",
    "mac": "FBGLM-HWG5O-FOWWK-JWRHC"
}

licenses_db = {}

def make_response(data):
    return Response(json.dumps(data), status=200, mimetype='application/json')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/appsumo/activate', methods=['POST', 'GET'])
def activate():
    if request.method == 'GET':
        return make_response({"message": "success", "redirect_url": RAILWAY_URL})
    data = request.json or {}
    license_key = data.get('license_key', '')
    licenses_db[license_key] = {'status': 'active', 'tier': data.get('tier', 1)}
    return make_response({"message": "success", "redirect_url": f"{RAILWAY_URL}/?license={license_key}"})

@app.route('/api/appsumo/deactivate', methods=['POST', 'GET'])
def deactivate():
    if request.method == 'GET':
        return make_response({"message": "success"})
    data = request.json or {}
    license_key = data.get('license_key', '')
    if license_key in licenses_db:
        licenses_db[license_key]['status'] = 'deactivated'
    return make_response({"message": "success"})

@app.route('/api/appsumo/enhance_tier', methods=['POST', 'GET'])
def enhance_tier():
    if request.method == 'GET':
        return make_response({"message": "success", "redirect_url": RAILWAY_URL})
    data = request.json or {}
    license_key = data.get('license_key', '')
    licenses_db[license_key] = {'status': 'active', 'tier': data.get('tier', 1)}
    return make_response({"message": "success", "redirect_url": f"{RAILWAY_URL}/?license={license_key}"})

@app.route('/api/appsumo/reduce_tier', methods=['POST', 'GET'])
def reduce_tier():
    if request.method == 'GET':
        return make_response({"message": "success"})
    data = request.json or {}
    license_key = data.get('license_key', '')
    if license_key in licenses_db:
        licenses_db[license_key]['tier'] = data.get('tier', 1)
    return make_response({"message": "success"})

@app.route('/api/redeem', methods=['POST'])
def redeem():
    data = request.json
    code = data.get('code', '').strip()
    system = data.get('system', '').lower()
    if not code:
        return jsonify({'success': False, 'message': 'Please enter your AppSumo code'})
    if system not in ['windows', 'mac']:
        return jsonify({'success': False, 'message': 'Please select a valid operating system'})
    return jsonify({'success': True, 'license_key': LICENSE_KEYS[system]})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
