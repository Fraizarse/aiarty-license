"""
Aiarty License Server for Replit
Compatible with AppSumo Licensing API v2
https://docs.licensing.appsumo.com/
"""

from flask import Flask, request, jsonify, send_file
import os
import json

app = Flask(__name__)

# License Keys
LICENSE_KEYS = {
    "windows": "FAKWB-BZWSM-UWEX4-IYF3C",
    "mac": "FBGLM-HWG5O-FOWWK-JWRHC"
}

# Store licenses (use database in production)
licenses_db = {}


@app.route('/')
def index():
    """Serve the frontend"""
    return send_file('index.html')


# ============================================
# AppSumo Required Endpoints
# ============================================

@app.route('/api/appsumo/notification', methods=['POST'])
def appsumo_notification():
    """
    Main notification endpoint for AppSumo
    Handles: activate, deactivate, upgrade, downgrade
    """
    data = request.json
    print(f"[AppSumo Notification] Received: {json.dumps(data, indent=2)}")
    
    action = data.get('action')
    plan_id = data.get('plan_id')
    uuid = data.get('uuid')
    activation_email = data.get('activation_email')
    invoice_item_uuid = data.get('invoice_item_uuid')
    
    response_data = {
        "message": "Success",
        "redirect_url": f"https://appsumo--Souhailkh.replit.app/?uuid={uuid}"
    }
    
    if action == 'activate':
        # New activation
        licenses_db[uuid] = {
            'uuid': uuid,
            'plan_id': plan_id,
            'email': activation_email,
            'invoice_item_uuid': invoice_item_uuid,
            'status': 'active'
        }
        print(f"[Activate] UUID: {uuid}, Plan: {plan_id}, Email: {activation_email}")
        return jsonify(response_data), 200
        
    elif action == 'deactivate':
        # Deactivation (refund)
        if uuid in licenses_db:
            licenses_db[uuid]['status'] = 'deactivated'
        print(f"[Deactivate] UUID: {uuid}")
        return jsonify({"message": "Success"}), 200
        
    elif action == 'upgrade':
        # Plan upgrade
        if uuid in licenses_db:
            licenses_db[uuid]['plan_id'] = plan_id
            licenses_db[uuid]['status'] = 'active'
        print(f"[Upgrade] UUID: {uuid}, New Plan: {plan_id}")
        return jsonify(response_data), 200
        
    elif action == 'downgrade':
        # Plan downgrade
        if uuid in licenses_db:
            licenses_db[uuid]['plan_id'] = plan_id
        print(f"[Downgrade] UUID: {uuid}, New Plan: {plan_id}")
        return jsonify(response_data), 200
    
    return jsonify({"message": "Success"}), 200


@app.route('/api/appsumo/activate', methods=['POST', 'GET'])
def activate():
    """
    Activation Event Endpoint
    Called when a user purchases and activates their license
    """
    # Handle GET request for AppSumo testing
    if request.method == 'GET':
        return jsonify({
            "message": "Success",
            "redirect_url": "https://appsumo--Souhailkh.replit.app/"
        }), 200
    
    data = request.json or {}
    print(f"[Activate Endpoint] Data: {json.dumps(data, indent=2)}")
    
    uuid = data.get('uuid', 'test')
    plan_id = data.get('plan_id', 'tier1')
    activation_email = data.get('activation_email', '')
    invoice_item_uuid = data.get('invoice_item_uuid', '')
    
    # Store the license
    licenses_db[uuid] = {
        'uuid': uuid,
        'plan_id': plan_id,
        'email': activation_email,
        'invoice_item_uuid': invoice_item_uuid,
        'status': 'active'
    }
    
    print(f"[Activated] UUID: {uuid}, Plan: {plan_id}, Email: {activation_email}")
    
    # Return redirect URL - Required by AppSumo
    return jsonify({
        "message": "Success",
        "redirect_url": f"https://appsumo--Souhailkh.replit.app/?uuid={uuid}"
    }), 200


@app.route('/api/appsumo/deactivate', methods=['POST', 'GET'])
def deactivate():
    """
    Deactivation Event Endpoint
    Called when a refund is processed
    """
    # Handle GET request for AppSumo testing
    if request.method == 'GET':
        return jsonify({"message": "Success"}), 200
    
    data = request.json or {}
    print(f"[Deactivate Endpoint] Data: {json.dumps(data, indent=2)}")
    
    uuid = data.get('uuid', '')
    
    # Mark license as deactivated
    if uuid and uuid in licenses_db:
        licenses_db[uuid]['status'] = 'deactivated'
    
    print(f"[Deactivated] UUID: {uuid}")
    
    return jsonify({
        "message": "Success"
    }), 200


@app.route('/api/appsumo/enhance_tier', methods=['POST', 'GET'])
def enhance_tier():
    """
    Purchase/Upgrade Event Endpoint
    Called when user upgrades their plan
    """
    # Handle GET request for AppSumo testing
    if request.method == 'GET':
        return jsonify({
            "message": "Success",
            "redirect_url": "https://appsumo--Souhailkh.replit.app/"
        }), 200
    
    data = request.json or {}
    print(f"[Enhance Tier Endpoint] Data: {json.dumps(data, indent=2)}")
    
    uuid = data.get('uuid', 'test')
    plan_id = data.get('plan_id', 'tier1')
    
    # Update the license
    if uuid in licenses_db:
        licenses_db[uuid]['plan_id'] = plan_id
        licenses_db[uuid]['status'] = 'active'
    else:
        licenses_db[uuid] = {
            'uuid': uuid,
            'plan_id': plan_id,
            'status': 'active'
        }
    
    print(f"[Enhanced] UUID: {uuid}, New Plan: {plan_id}")
    
    return jsonify({
        "message": "Success",
        "redirect_url": f"https://appsumo--Souhailkh.replit.app/?uuid={uuid}"
    }), 200


@app.route('/api/appsumo/reduce_tier', methods=['POST', 'GET'])
def reduce_tier():
    """
    Downgrade Event Endpoint
    Called when user downgrades their plan
    """
    # Handle GET request for AppSumo testing
    if request.method == 'GET':
        return jsonify({"message": "Success"}), 200
    
    data = request.json or {}
    print(f"[Reduce Tier Endpoint] Data: {json.dumps(data, indent=2)}")
    
    uuid = data.get('uuid', '')
    plan_id = data.get('plan_id', '')
    
    # Update the license
    if uuid and uuid in licenses_db:
        licenses_db[uuid]['plan_id'] = plan_id
    
    print(f"[Reduced] UUID: {uuid}, New Plan: {plan_id}")
    
    return jsonify({
        "message": "Success"
    }), 200


# ============================================
# Frontend API Endpoints
# ============================================

@app.route('/api/redeem', methods=['POST'])
def redeem():
    """Redeem AppSumo code and get license key"""
    data = request.json
    code = data.get('code', '').strip()
    system = data.get('system', '').lower()
    
    if not code:
        return jsonify({
            'success': False,
            'message': 'Please enter your AppSumo code'
        })
    
    if system not in ['windows', 'mac']:
        return jsonify({
            'success': False,
            'message': 'Please select a valid operating system'
        })
    
    # Check if UUID exists in our database
    license_data = licenses_db.get(code)
    
    if license_data and license_data.get('status') == 'deactivated':
        return jsonify({
            'success': False,
            'message': 'This license has been deactivated or refunded'
        })
    
    # Return license key
    license_key = LICENSE_KEYS[system]
    
    return jsonify({
        'success': True,
        'license_key': license_key,
        'message': f'Your Aiarty license key for {system}'
    })


@app.route('/api/check/<uuid>', methods=['GET'])
def check_license(uuid):
    """Check license status"""
    if uuid in licenses_db:
        return jsonify({
            'valid': True,
            'status': licenses_db[uuid].get('status'),
            'plan_id': licenses_db[uuid].get('plan_id')
        })
    return jsonify({'valid': False}), 404


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


# Test endpoint to verify setup
@app.route('/api/test', methods=['GET', 'POST'])
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'working',
        'method': request.method,
        'message': 'AppSumo integration is ready!'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
