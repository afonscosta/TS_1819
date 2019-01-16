#! /usr/bin/env python3

import smtplib, ssl
import re
import os
import string
import sys
import random
from random import randrange

def send_email(pw, to_addrs):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "ts.1819.teste@gmail.com"
    password = "tecseg1819"
    message = 'To: {}\r\nSubject: {}\r\n\r\n{}'.format(to_addrs.rstrip(), 'Password do ficheiro', pw)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, [to_addrs], message)



with open(os.getenv("HOME") + "/.database.txt", "r") as fd:
    for line in fd:
        info = re.split(r'::', line)
        if sys.argv[1] == info[0]:
            to_addrs = info[1]
            n = randrange(10, 21)
            newpass = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(n))
            print(newpass)
            send_email(newpass, to_addrs)
            break
