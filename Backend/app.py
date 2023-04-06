import os
from flask import Flask, render_template, request, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__),
template_folder=os.path.abspath('../frontend/templates'),
static_folder=os.path.abspath('../frontend/static'))
alerts = {}

EMAIL_ADDRESS = "yourpricealerts@gmail.com"
EMAIL_PASSWORD = "bnzyctvnlpykusaa"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Use 465 for SSL

def send_email(email, coin, price):
    msg = MIMEMultipart()
    msg['Subject'] = f'Crypto Alert: {coin}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.attach(MIMEText(f'{coin} is: {price}', 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
            print(f'Sent alert to {email} for {coin} at price {price}')
    except Exception as e:
        print(f'Error sending email: {e}')


def fetch_price(coin):
    coin = coin.upper()
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={coin}"
    response = requests.get(url)
    data = response.json()
    return float(data['data']['price'])


def alert_job():
    for email, alert in alerts.items():
        for coin, interval_info in alert.items():
            interval_info['counter'] -= 1
            if interval_info['counter'] <= 0:
                price = fetch_price(coin)
                send_email(email, coin, price)
                interval_info['counter'] = interval_info['interval']


scheduler = BackgroundScheduler()
scheduler.add_job(alert_job, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    data = request.get_json()
    email = data['email']
    coin = data['coin']
    interval = int(data['interval'])

    if email not in alerts:
        alerts[email] = {}

    alerts[email][coin] = {'interval': interval, 'counter': interval}
    return jsonify({'status': 'success'})


@app.route('/api/alerts', methods=['DELETE'])
def delete_alert():
    data = request.get_json()
    email = data['email']
    coin = data['coin']

    if email in alerts and coin in alerts[email]:
        del alerts[email][coin]

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
