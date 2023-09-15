import requests
import smtplib
from datetime import datetime
import time
MY_LAT = 28.704060
MY_LNG = 77.102493


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    iss_position = (longitude, latitude)
    if MY_LAT-5 <= latitude <= MY_LAT+5 and MY_LNG-5 <= longitude <= MY_LNG+5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted" : 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    timenow = datetime.now().hour
    if timenow >= sunset or timenow <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_dark() and is_iss_overhead():
        email = ["your email"]
        password=["your password"]
        recievers_email = ["mohit.bhatt.work@gmail.com"]
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        s.login(email, password)

        # message to be sent
        message = "Subject: Look up👆\n\nThe International Space Station is Above your location. !"

        # sending the mail
        for mail in recievers_email:
            s.sendmail(email, mail , message)
        # terminating the session
        s.quit()
        print("email sent")

    else:
        print("not overhead")