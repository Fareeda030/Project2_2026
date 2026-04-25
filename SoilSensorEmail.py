import RPi.GPIO as GPIO
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime

from_email_addr="2959937619@qq.com"
from_email_pass="fpqwqsfgezkodehe"
to_email_addr="19101967@qq.com"

channel=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)

SMTP_SERVER="smtp.qq.com"
SMTP_PORT=587

DRY_LEVEL=1

CHECK_HOURS=[8,13,17,21]

def send_mail(plant_status):
	try:
		msg=EmailMessage()
		msg.set_content(f"Plant Status:{plant_status}")
		msg['From']=from_email_addr
		msg['To']=to_email_addr
		msg['Subject']='PLANT STATUS REMINDER'
		server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
		server.starttls()
		server.login(from_email_addr,from_email_pass)
		server.send_message(msg)
		server.quit()
	except Exception as e:
		print(f"Failed:{e}")

def read_sensor():
	value = GPIO.input(channel)
	return value == DRY_LEVEL
last_sent_hour = -1
try:
	while True:
		now=datetime.now()
		now =datetime.now()
		current_hour=now.hour
		if current_hour in CHECK_HOURS and current_hour!=last_sent_hour:
			need_water=read_sensor()
			print(f"need_water={need_water}")
			if need_water:
				send_mail("Dry.\nPlease water your plant.")
				print(f"[{now}] Dry,a notification email was sent.")
			else:
				send_mail("Wet.\nWater NOT needed.")
				print(f"[{now}] Wet,a notification email was sent.")
			last_sent_hour=current_hour

		if current_hour!=last_sent_hour and current_hour not in CHECK_HOURS:
			last_sent_hour=-1


		time.sleep(5)
except KeyboardInterrupt:
	print("The program is manually interrupted.")
finally:
	GPIO.cleanup()





