# ProjectResearch_SPearPhishing



In this project repository we have the getgmail python file to get contents of gmail



Steps to execute:

1.STart smptp server:
python -m smtpd -n -c DebuggingServer localhost:1025

2.Execute python file 
./SimpleEmailSpoofer.py -e send_email.html -t random@gmail.com -f harshbajaj.rules@gmail.com -n "Jason Polakis" -j "Regarding CS 597" -p 1025
(For address spoofing)

./SimpleEmailSpoofer.py -e send_email.html -t random@gmail.com -f harsh.rocks@hotmail.com -n "Random  Person" -j "Regarding CS 597" -p 1025

(for name spoofing)

3.Bro tool execution for link logging with payload as twitter.pcap


bro -r twitter.pcap smtp-url.bro 


Here twitter.pcap contains my urls and has the timestamp information.We can create this pcap using Wireshark
