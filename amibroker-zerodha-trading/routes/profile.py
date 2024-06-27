from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from kiteconnect import KiteConnect
from dotenv import dotenv_values
para = {key: value for key, value in dotenv_values('.env').items()}



def create_profile_blueprint(db, kite):
    profile_bp = Blueprint('profile', __name__)    
    
    @profile_bp.route('/login')
    def login():
        # Get the login URL
        login_url = kite.login_url()
        return redirect(login_url)

    @profile_bp.route('/login/callback')
    def login_callback():
        request_token = request.args.get('request_token')
        print(request_token)
        if request_token:
            # Generate session and get access token
            try:
                data = kite.generate_session(request_token, api_secret=para["api_key"])
                if data.get('access_token'):
                    kite.set_access_token(data['access_token'])
                    session['access_token'] = data["access_token"]
                    # session['public_token'] = data["public_token"]
                    session['user_id'] = data["user_id"]
                    db.create_user(data["user_id"], para["api_key"])
                    flash('Login successful!', 'success')
                    return redirect(url_for('profile'))
            except Exception as e:
                flash('Login failed: ' + str(e), 'danger')
        return redirect(url_for('index'))

    @profile_bp.route('/profile', methods=['GET'])
    def profile():
        try:
            #Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            
            # kite.set_access_token(access_token)

            # Fetch the profile
            profile = kite.profile()
            return jsonify(profile)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return profile_bp