import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import smtplib
import warnings
import random
import platform
import sys
from termcolor import colored
from colorama import Fore, init
import os
from datetime import datetime, timedelta
import json

init()

bl, wh, yl, red, gr, ble, cy, bwh, byl, bred, bgr = Fore.BLACK, Fore.WHITE, Fore.YELLOW, Fore.RED, Fore.GREEN, Fore.BLUE, Fore.CYAN, Fore.WHITE, Fore.YELLOW, Fore.RED, Fore.GREEN
init()
def print_logo():
    print(Fore.RED + """
                   Contact https://t.me/STORMTOOLS101  STORM BY BIGGEST V8\n
                     █████   █████  █████  █████   █████  █████  █████
                     █    █    █    █      █       █      █        █
                     █████     █    █  ███ █  ███  ████    ███     █ 
                     █    █    █    █    █ █    █  █          █    █  
                     █████   █████   █████  █████  █████  ████     █\033[0m 

                               E-MAIL SENDER---------- V8
""")
    print(f"                        Date and Time: {Fore.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{Fore.RESET}")
init()
def calculate_expiration_date(time_frame):
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=time_frame)
    return expiration_date.strftime("%Y-%m-%d")

def get_machine_id():
    machine_id = platform.node()
    return machine_id

def authenticate_user(user_id, token):
    base_url = 'https://thereplys.net/api/'  

    url = base_url + 'user.json'
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        machine_count = 0

        for user_info in user_data:
            if user_info['user_id'] == user_id and user_info['token'] == token:
                machine_count = len(user_info.get('machines', []))

                if machine_count >= user_info['machine_limit']:
                    return "Machine limit reached. CONTACT https://t.me/STORMTOOLS101."
                machine_name = get_machine_id()
                if machine_name not in user_info.get('machines', []):
                    user_info['machines'] = user_info.get('machines', []) + [machine_name]
                    machine_count += 1

                    with open('user_info.json', 'w') as file:
                        json.dump({'user_id': user_id, 'token': token}, file)
                    
                expiration_date = datetime.strptime(user_info.get('expiration_date', calculate_expiration_date(user_info['time_frame'])), "%Y-%m-%d")

                if expiration_date < datetime.now():
                    return "Your access has expired. CONTACT https://t.me/STORMTOOLS101."
                
                welcome_message = f"ACCESS GRANTED!\n\nWelcome {user_id}!\nMachine limit: {user_info['machine_limit']}\nExpiration date: {expiration_date.strftime('%Y-%m-%d')}"
                return welcome_message

        return "Invalid user ID or token. CONTACT https://t.me/STORMTOOLS101."
    else:
        return "Error fetching user data from the server."

def read_reply_to_email():
    reply_to_file = "reply-to.txt"
    if os.path.exists(reply_to_file):
        with open(reply_to_file, 'r') as file:
            return file.read().strip()
    else:
        print("Reply-to email file not found. Please create a file named 'reply-to.txt' with the reply-to email address.")
        return     

def read_smtp_info():
    smtp_info_file = "smtp.txt"
    if os.path.exists(smtp_info_file):
        with open(smtp_info_file, 'r') as file:
            smtp_info = file.read().strip().split('|')
            return smtp_info
    else:
        print("SMTP info file not found. Please create a file named 'smtp.txt' with your SMTP information.")
        return 

def read_message():
    message_file = "message.txt"
    if os.path.exists(message_file):
        with open(message_file, 'r', encoding="utf-8") as file:
            return file.read()
    else:
        print("Message file not found. Please create a file named 'message.txt' with your SMS message.")
        return 

def read_sender_email():
    sender_email_file = "sender-email.txt"
    if os.path.exists(sender_email_file):
        with open(sender_email_file, 'r') as file:
            return file.read().strip()
    else:
        print("Sender email file not found. Please create a file named 'sender-email.txt' with the sender's email address.")
        return None

def read_message(content_type):
    file_name = "message.txt" if content_type == 'text' else 'html.txt'
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return file.read().strip()
    else:
        print(f"{file_name} not found. Please create this file with the message content.")
        return 

def send_email(phone_number, message, smtp_info, domain, sender_email, reply_to_email, subject, security_type, content_type):
    try:
        smtp_server, smtp_port, smtp_user, smtp_password = smtp_info
    except ValueError:
        print("Invalid SMTP information format. Please check the 'smtp.txt' file.")
        return

    email_domain = f"@{domain}"
    email_address = phone_number + email_domain

    if content_type == 'text':
        msg = MIMEText(message)
    elif content_type == 'html':
        msg = MIMEMultipart()
        msg.attach(MIMEText(message, 'html'))
    else:
        print("Invalid content type. Please choose 'text' or 'html'.")
        return

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email_address
    msg.add_header('reply-to', reply_to_email)

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            if security_type == "TLS":
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(Fore.GREEN + f"Email sent to {email_address}" + Fore.RESET)
    except smtplib.SMTPException as e:
        print(Fore.RED + f"Failed to send Message to {email_address}: {e}" + Fore.RESET)

init()     
def send_email(phone_number, html_content, smtp_info, domain, sender_email, reply_to_email, subject, security_type):
    try:
        smtp_server, smtp_port, smtp_user, smtp_password = smtp_info
    except ValueError:
        print("Invalid SMTP information format. Please check the 'smtp.txt' file.")
        return

    email_domain = f"@{domain}"
    email_address = phone_number + email_domain

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email_address
    msg.add_header('reply-to', reply_to_email)

    part2 = MIMEText(html_content, 'html')
    msg.attach(part2)
    init()
    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            if security_type == "TLS":
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            print(Fore.GREEN + f"Email sent to {email_address}" + Fore.RESET)
    except smtplib.SMTPException as e:
        print(Fore.RED + f"Failed to send email to {email_address}: {e}" + Fore.R)

        
    init()
def main():
    init()
    print_logo()
    user_info_file = 'user_info.json'
    user_id, token = None, None
    if os.path.isfile(user_info_file):
        with open(user_info_file, 'r') as file:
            user_info = json.load(file)
            user_id = user_info.get('user_id')
            token = user_info.get('token')

    if not user_id or not token:
        user_id = input("Enter User ID: ")
        token = input("Enter Token: ")
        print("")
        result = authenticate_user(user_id, token)
        if result and result.startswith("ACCESS GRANTED!"):
            print(Fore.GREEN + result)  
            print("")
        else:
            print(Fore.RED + "Authentication failed. Please check your User ID and Token or Contact https://t.me/STORMTOOLS101." + Fore.RESET)
            return
    numbers_with_domains_path = input("input Email path: ")
    print("")

    if os.path.exists(numbers_with_domains_path):
        with open(numbers_with_domains_path, 'r') as file:
            numbers_with_domains = [line.strip() for line in file.readlines()]
    else:
        print("Emails file not found. Please create a file with emails in 'email@domain.com' format.")
        return

    sender_name = input('Enter the Sender Name: ')
    sender_email = read_sender_email()
    sender_email_full = f"{sender_name} <{sender_email}>"
    print("")

    reply_to_email = read_reply_to_email()

    subject = input('Enter the Subject: ')
    print("")

    print("Select the security type:")
    print("1. TLS")
    print("2. SSL")
    choice = input("Enter your choice (1/2): ")
    print("")
    security_type = "TLS" if choice == '1' else "SSL"

    smtp_info_file = "smtp.txt"
    if os.path.exists(smtp_info_file):
        with open(smtp_info_file, 'r') as file:
            smtp_info = file.read().strip().split('|')
    else:
        print("SMTP info file not found. Please create a file named 'smtp.txt' with your SMTP information.")
        return

    html_content_path = 'html.txt'
    print("")
    print(Fore.GREEN + 'SENDING YOU!!' + Fore.RESET)
    print("")
    print("")
    with open(html_content_path, 'r') as html_file:
        html_content = html_file.read()

    for item in numbers_with_domains:
        phone_number, domain = item.split('@')
        send_email(phone_number, html_content, smtp_info, domain, sender_email_full, reply_to_email, subject, security_type)
        
if __name__ == "__main__":
    main()
    print("")
    print("")
    print (Fore.GREEN, f"THANKs TO BIGGEST")
    input('Press Enter to close...')
    sys.exit()
