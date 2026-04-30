from flask import Flask, render_template, request, redirect, session
import random
import time

app = Flask(__name__)
app.secret_key = "secret123"

USERNAME = "admin"
PASSWORD = "1234"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')

        if user == USERNAME and pwd == PASSWORD:
            otp = str(random.randint(1000, 9999))
            session['otp'] = otp
            session['otp_time'] = time.time()

            # 🔥 OTP terminal me clearly print hoga
            print("\n======================")
            print("🔐 YOUR OTP IS:", otp)
            print("======================\n")

            return render_template('otp.html')

        else:
            return render_template('login.html', error="Invalid Credentials ❌")

    return render_template('login.html')


@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp')

    if 'otp' not in session:
        return "OTP not found ❌"

    if time.time() - session['otp_time'] > 60:
        return "OTP Expired ❌"

    if user_otp == session['otp']:
        session.clear()
        return render_template('dashboard.html')
    else:
        return "Wrong OTP ❌"


if __name__ == '__main__':
    app.run(debug=True)