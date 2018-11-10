import smtplib
import time
import imaplib
import email
import webbrowser
import re
import os
from datetime import datetime
import json
import sys
from parsebrologs import ParseBroLogs
import mysql.connector
import sched, time

s = sched.scheduler(time.time, time.sleep)
starttime=time.time()
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------



def read_email_from_gmail():

    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        typ, data = mail.search(None, 'ALL','(UNSEEN)')
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print "FIrst",first_email_id
        print "latest",latest_email_id
      
        #date = (datetime.date.today() - datetime.timedelta(5)).strftime("%d-%b-%Y")
        #print date
        #result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))

        """

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
        """    
        body=''
        httpsurls=[]
        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            #mail.store(data[0][1].replace(' ',','),'+FLAGS','\Seen')
            #print raw_email_string
            email_message = email.message_from_string(raw_email_string)
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_email=email_from.split('<', 1)[1].split('>')[0]
                    email_name=email_from.split('<')[0]
                    mydb = mysql.connector.connect(host="37.60.252.244",user="engageil_com",password="iQmFqxG0crZo", database="engageil_com")
                    c = mydb.cursor()
                    try:
                       c.execute("INSERT INTO Email_Spoof(Name,Email) VALUES('%s','%s')" % (email_name,email_email))
                       mydb.commit()
                    except:
                       res = c.execute("""SELECT name,email from Email_Spoof where email = '%s' """ % (e,))
                       print "I have already seen this email address with different Name",str(c.fetchone()[1]) 
                    #print msg
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
                    #print  'From Email : ' + email_email + '\n'
            for part in email_message.walk():
                if part.get_content_type() == "text/plain": # ignore attachments/html
                   body = part.get_payload(decode=True)
                   print 'Body : <a href =\' ' + body     +'\''
                   url='www.kaggle.com'
                   new = 2 # open in a new tab, if possible

                   
                   httpsurls = re.findall("(?P<url>https?://[^\s]+)", body)     
                   for urls in re.findall("(?P<url>https?://[^\s]+)", body):
                       webbrowser.open(urls,new=new) 
                   httpsurls = re.findall("(?P<url>http?://[^\s]+)", body)     
                   for urls in re.findall("(?P<url>http?://[^\s]+)", body):
                       webbrowser.open(urls,new=new)  
                os.system("bro -r eth1_data.pcap local smtp-url.bro \"Site::local_nets += { 10.0.0.0/8 }\"") 
                os.system("bro -r eth1_data.pcap local smtp-url.bro \"Site::local_nets += { 10.0.0.0/8 }\"")
                  
                   #webbrowser.open(url,new=new)

                log_data = ParseBroLogs("dns.log",fields=["ts", "uid","id.orig_h", "id.resp_h","query"])
                with open('out_demo2.json',"w") as outfile:
                      outfile.write(log_data.to_json())
                with open('out_demo2.json') as f:
                      data = json.load(f)
                      url='www.google.com'
                      for i in range(1,len(data)):
                          host_name=str(data[i]["query"])
                          print  datetime.fromtimestamp(float(data[i]["ts"])).strftime("%Y-%m-%d %H:%M"),",",str(data[i]["query"])  
                          
                          mydb = mysql.connector.connect(host="37.60.252.244",user="engageil_com",password="iQmFqxG0crZo", database="engageil_com")
                          c = mydb.cursor()
                          try:
      
                              c.execute("INSERT INTO URL_Bro_parser(URL,timestamp) VALUES('%s','%s')" % (url,datetime.fromtimestamp(float(data[i]["ts"])).strftime("%Y-%m-%d %H:%M")))
                              mydb.commit()
                          except:
                            print "Exception"
                          
                log_data_http = ParseBroLogs("http.log",fields=["user_agent", "hosturi","referrer"])
                with open('out_demo_http.json',"w") as outfile:
                       outfile.write(log_data_http.to_json()) 
                with open('out_demo_http.json') as f:
                       data = json.load(f)
                       for i in range(1,len(data)):
                           host_name=str(data[i]["hosturi"])                       

        threading.Timer(25.0, read_email_from_gmail).start()
# open an HTML file on my own (
    except Exception, e:
        print str(e)
if __name__ == "__main__":  
   ORG_EMAIL   = "@gmail.com"
   FROM_EMAIL  = "harshbajaj.rules" + ORG_EMAIL
   FROM_PWD    = "zkwqwvkdfproqmfj"
   SMTP_SERVER = "imap.gmail.com"
   SMTP_PORT   = 993    

  
   read_email_from_gmail()