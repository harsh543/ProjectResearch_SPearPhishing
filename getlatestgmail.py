#import smtplib
import time
import imaplib
import email
import webbrowser
import re
import datetime
from datetime import date
from datetime import timedelta
import threading
import os
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
        your_timestamp=1541742685.443735
        prev_date=datetime.datetime.fromtimestamp(your_timestamp).date()
        print  type(prev_date)
        today=datetime.date.today()
        date = (datetime.date.today() - datetime.timedelta((today-prev_date).days)).strftime("%d-%b-%Y")
        print date
        typ, data = mail.search(None, 'ALL','(UNSEEN)',"(SINCE {0})".format(date))
        
        mail_ids = data[0]

        id_list = mail_ids.split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print "FIrst",first_email_id
        print "latest",latest_email_id
        #mail.store(data[0].replace(' ',','),'+FLAGS','\Seen')
        #date = (datetime.date.today() - datetime.timedelta(5)).strftime("%d-%b-%Y")
        #print date
        #result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))

        """

        for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
        """    
        body=''
        httpsurls=[]
        for i in id_list:
            typ, data = mail.fetch(i, '(RFC822)' )
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            mail.store(i, '+FLAGS', '\\Seen')
            #print raw_email_string
            email_message = email.message_from_string(raw_email_string)
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    from_header=msg['from']
                    from_name=from_header.rsplit('<', 1)[0]
                    print msg["to"]
                    email_from = re.search(r'\<(.*?)\>',from_header).group(1)
                    #print msg
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'
            for part in email_message.walk():
                if part.get_content_type() == "text/plain": # ignore attachments/html
                   body = part.get_payload(decode=True)
                   print 'Body : <a href =\' ' + body     +'\''
                   url='www.kaggle.com'
                   new = 2 # open in a new tab, if possible
                   if re.search("(?P<url>https?://[^\s]+)", body):
                      url = re.search("(?P<url>https?://[^\s]+)", body).group("url") 
                      #webbrowser.open(url,new=new)
                   elif re.search("(?P<url>https?://[^\s]+)", body):
                        url = re.search("(?P<url>https?://[^\s]+)", body).group("url") 
                        #webbrowser.open(url,new=new)
                   
                   httpsurls = re.findall("(?P<url>https?://[^\s]+)", body)     
                   for urls in re.findall("(?P<url>https?://[^\s]+)", body):
                       webbrowser.open(urls,new=new) 
                   httpsurls = re.findall("(?P<url>http?://[^\s]+)", body)     
                   for urls in re.findall("(?P<url>http?://[^\s]+)", body):
                       webbrowser.open(urls,new=new) 
                   os.system("bro -r eth1_data.pcap local smtp-url.bro \"Site::local_nets += { 10.0.0.0/8 }\"") 
                   os.system("bro -r eth1_data.pcap local smtp-url.bro \"Site::local_nets += { 10.0.0.0/8 }\"")     
        threading.Timer(25.0, read_email_from_gmail).start()               
                   
            
# open an HTML file on my own (
    except Exception, e:
          print str(e)
          threading.Timer(25.0, read_email_from_gmail).start()
if __name__ == "__main__":  
   ORG_EMAIL   = "@gmail.com"
   FROM_EMAIL  = "harshbajaj.rules" + ORG_EMAIL
   FROM_PWD    = "zkwqwvkdfproqmfj"
   SMTP_SERVER = "imap.gmail.com"
   SMTP_PORT   = 993      
   read_email_from_gmail()