import smtplib

# Import the email modules we'll need
# me == the sender's email address
# you == the recipient's email address
FROM = x
TO = y
SUBJECT = 'subject'
TEXT = 'body'

# Prepare actual message
message = """From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)


server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(x, z)
server.sendmail(x, y, message)
server.close()
