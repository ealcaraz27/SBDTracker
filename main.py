from bs4 import BeautifulSoup
from email.message import EmailMessage
from datetime import datetime
import json
import smtplib
import requests
import time

log_file = "log.txt"

def log_entry(message):
    with open(log_file, "a") as file:
        timelog = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timelog} - {message}\n")

def check_availability(url, phrase):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if phrase in soup.text:
            log_entry("Available for purchase!")
            return True
        else:
            return False
    except Exception as e:
        log_entry(f"Error on parsing website: {str(e)}")

def send_email(url, config):
    msg = EmailMessage()
    msg['Subject'] = "SBD Belt Tracker"
    msg['From'] = config["sender_email"]
    msg['To'] = config["receiver_email"]
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>In-Stock Alert</title>
    </head>
    <body>
        <table width="100%" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center" style="background-color: #f4f4f4; padding: 20px;">
                    <table width="600" cellspacing="0" cellpadding="0">
                        <tr>
                            <td align="center" style="background-color: #ffffff; padding: 40px;">
                                <h1>In-Stock Alert</h1>
                                <p>SBD Belt is now in stock!</p>
                                <a href="https://us.sbdapparel.com/products/13mm-lever-belt?variant=39569223876765" style="display: inline-block; background-color: #007BFF; color: #ffffff; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">BUY NOW</a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>"""
    msg.set_content(html_content, subtype='html')

    try:
        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
        server.starttls()
        server.login(config["sender_email"], config["app_pass"])
        
        server.send_message(msg)
        log_entry("Message sent!")
        print("Email Sent Successfully!")
    except Exception as e:
        log_entry("Error sending message ")
        print(f"An error occured: {str(e)}")
    finally:
        server.close()

def main():
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)
    url = "https://us.sbdapparel.com/products/13mm-lever-belt?variant=39569223876765"
    phrase = "2XL - $280.00 USD"

    while True:
        available = check_availability(url, phrase)
        if available == True:
            print("In Stock!")
            send_email(url,config)
        if available == False:
            print("Sold Out!")
        time.sleep(300)
        # break # uncomment out line if you want program to only run once


if __name__ == '__main__':
    main()

