from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv
import logging
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv() 

app = Flask(__name__)
subscriptions = [] 

SENDER_EMAIL_ADDRESS = os.getenv('SENDER_EMAIL_ADDRESS') 
SENDER_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD') 
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587 

logger = logging.getLogger(__name__) 
handler = logging.StreamHandler() 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
handler.setFormatter(formatter)  
logger.addHandler(handler) 

@app.route('/', methods=['GET']) 
def index():
    return render_template('index.html', subscriptions=subscriptions)

@app.route('/subscribe', methods=['POST']) 
def subscribe():
    email = request.form['email'] 
    url = request.form['url'] 
    if not any(email == sub[0] and url == sub[1] for sub in subscriptions): 
        subscriptions.append((email, url)) 
    return render_template('subscribe.html') 

scheduler = BackgroundScheduler() 

@scheduler.scheduled_job('interval', seconds=10) 
def check_websites():
    print("Checking websites...")
    for email, url in subscriptions:
        try:
            response = requests.get(url) 
            if response.status_code != 200: 
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) 
                msg = f'Subject: Your Website Status\n\nThe website {url} is down.'
                server.starttls() # Start the TLS connection
                server.login(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_PASSWORD) 
                server.sendmail(SENDER_EMAIL_ADDRESS, email, msg) 
                server.quit() 
                logger.info(f'Email sent to {email} for website {url}') 
        except Exception as e:
            logger.error(f'Error sending email to {email} for website {url}: {e}') 

if __name__ == '__main__':
    scheduler.start() 
    app.run(debug=True) 