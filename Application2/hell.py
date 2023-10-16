import smtplib
import ssl
from email.message import EmailMessage
OTP = "9769"
mailid="prabhath1709@gmail.com"
email_sender = 'dlsathwik@gmail.com'
email_password = 'wnfppwzpxswzryqy'
email_receiver =  mailid
car=smtplib.SMTP("smtp.gmail.com",587)
car.starttls()
car.login(email_sender,email_password)
car.sendmail(from_addr=email_sender,to_addrs=email_receiver,msg="hiiiiiiii")
car.close()