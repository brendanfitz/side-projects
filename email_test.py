#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, ssl

port = 465  # For SSL

sender_email = input("Type your sender email and press enter: ")
receiver_email = input("Type your receiver email and press enter: ")
password = input("Type your password and press enter: ")
message = """\
Subject: Hi there from Python!

This message is from python! Python rulezzzzz"""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
