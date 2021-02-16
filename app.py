import openpyxl
from openpyxl import load_workbook as lwb
import http.client
import urllib.parse
import json
import googlemaps
import re

from sensitive import gmapsKey, gmailPassword, sender_address, northEmail, southEmail, eastEmail, westEmail

import smtplib, email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#Constants
N_MIN_LAT = 32.100766
E_MIN_LAT_A = 32.064696
E_MAX_LAT_A = 32.079732
E_MIN_LON_A = 34.793462
E_MAX_LAT_B = 32.064696
E_MIN_LON_B = 34.785705
S_MAX_LAT = 32.069
S_MAX_LON = 34.786273

#conn = http.client.HTTPConnection('api.positionstack.com')
gmaps = googlemaps.Client(key=gmapsKey)
northWorkerMail = ""
westWorkerMail = ""
southWorkerMail = ""
eastWorkerMail = ""
mails = [northWorkerMail, westWorkerMail, southWorkerMail, eastWorkerMail]
errors = []
errorsMail = ""

northURL = ["http://maps.google.com/maps?"]
eastURL = ["http://maps.google.com/maps?"]
westURL = ["http://maps.google.com/maps?"]
southURL = ["http://maps.google.com/maps?"]

def URL_Encoded_add(workerURL ,address):
    encodedAddress = re.sub('\W+',' ', address)
    encodedAddress = encodedAddress.replace(" ", "+")
    if "saddr" not in workerURL[0]:
        print ("adding saddr: ")
        workerURL[0]+="saddr="+encodedAddress
    elif "daddr" not in workerURL[0]:
        print ("adding daddr: ")
        workerURL[0]+= "&daddr=" + encodedAddress
    elif "daddr" in workerURL[0]:
        print ("adding to: ")
        workerURL[0]+= "+to:" + encodedAddress
    print(encodedAddress)
    print(workerURL[0])

# getting the adresses from Excel file
print ("getting adresses")
wb = lwb('שאלתא לישיבה.xlsx')
ws = wb.active
max_row = ws.max_row
for i in range(1, max_row+1):  # TODO: Search for the Death_street&Street_number columns
    dateDead = ws.cell(row=i, column=1)
    familyName = ws.cell(row=i, column=2)
    firstName = ws.cell(row=i, column=3)
    street = ws.cell(row=i, column=4)
    street_num = ws.cell(row=i, column=5)
    city = ws.cell(row=i, column=6)
    deadConection = ws.cell(row=i, column=7)
    phone = ws.cell(row=i, column=8)
    adressString = str(street.value)+" "+str(street_num.value)+" "+str(city.value)
    mail =  "כתובת: {} \n שם: {} שם משפחה:{} \n תאריך: {} \n טלפון: {} קרבה: {} \n\n".format(adressString, firstName.value, familyName.value, dateDead.value, phone.value, deadConection.value)
    mails.append(mail)
    print(mail)

    if adressString == "None None None":
        continue
    else:

# Forward geocoding the adresses
        try:  
            res = gmaps.geocode(adressString)  # conn.getresponse()
            lat = float(res[0]['geometry']['location']['lat'])
            print(lat)
            lon = float(res[0]['geometry']['location']['lng'])
            print(lon)

            #Sort the adresses by workers
            #Sorting addresses for North Worker
            if lat > N_MIN_LAT: 
                northWorkerMail+=mail
                URL_Encoded_add(northURL,adressString)
                print(adressString,"added to URL")
                print(adressString+" added to north")
            #Sorting addresses for East Worker
            elif (E_MIN_LAT_A < lat <= E_MAX_LAT_A and lon >= E_MIN_LON_A) or (lat < E_MAX_LAT_B and lon > E_MIN_LON_B):
                eastWorkerMail+=mail
                URL_Encoded_add(eastURL,adressString)
                print(adressString+" added to east")
            #Sorting addresses foB South Worker
            elif lat < S_MAX_LAT  and lon < S_MAX_LON:
                URL_Encoded_add(southURL,adressString)
                southWorkerMail+=mail
                print(adressString+" added to south")
            #Sorting addresses for West Worker
            else:
                westWorkerMail+=mail
                URL_Encoded_add(westURL,adressString)
                print(adressString+" added to west")
        except:
            print("Error occurred")
            errors.append(adressString)
northWorkerMail+= "קישור: "+northURL[0]+"\n"
eastWorkerMail+= "קישור: "+eastURL[0]+"\n"
westWorkerMail+= "קישור: "+westURL[0]+"\n"
southWorkerMail+="קישור: "+southURL[0]+"\n"
print("*צפון*")
print(northWorkerMail)
print("*דרום*")
print(southWorkerMail)
print("*מרכז*")
print(westWorkerMail)
print("*מזרח*")
print(eastWorkerMail)
print("*לא התמיין*")
print(errors)

def send_mail(workerEmail, content, zone):
  #The mail addresses and password
  receiver_address = workerEmail
  #Setup the MIME
  message = MIMEMultipart()
  message['From'] = sender_address
  message['To'] = receiver_address
  message['Subject'] =  zone   #The subject line
  #The body and the attachments for the mail
  mail_content = content
  message.attach(MIMEText(mail_content, 'plain'))
  #Create SMTP session for sending the mail
  session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
  session.starttls() #enable security
  session.login(sender_address, gmailPassword) #login with mail_id and password
  text = message.as_string()
  session.sendmail(sender_address, receiver_address, text)
  session.quit()
print ("sending mails")
send_mail(northEmail,northWorkerMail, " צפון ")
print("mail sent to north Worker")
send_mail(northEmail,eastWorkerMail, " מזרח ")
print("mail sent to east Worker")
send_mail(westEmail,westWorkerMail, " מרכז ")
print("mail sent to west Worker")
send_mail(southEmail,southWorkerMail, " דרום ")
print("mail sent to south Worker")
#send_mail(office@ytlv.co.il,"הכתובות הבאות נשלחו באופן אוטומטי למיילים של העובדים\n"+northWorkerMail+eastWorkerMail+southWorkerMail+westWorkerMail, "כתובות אוטומתי")
print("mails sent")