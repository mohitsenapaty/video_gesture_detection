import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate



email_id = "forkbombers10@gmail.com"
email_pwd = "Bombers@10"



#Send the mail  
def send_email(msg_txt, sub, attach=None):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

#Next, log in to the server
    server.login(email_id, email_pwd)
    msg = MIMEMultipart()
    msg['From'] = email_id
    msg['To'] = email_id
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = sub

    msg.attach(MIMEText(msg_txt))
    #import pdb; pdb.set_trace();
    for f in attach or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    val = server.sendmail(email_id, email_id, msg.as_string())
    server.close()
    return val

def send_email_client(to, msg_txt, sub, attach=None):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

#Next, log in to the server
    server.login(email_id, email_pwd)
    msg = MIMEMultipart()
    msg['From'] = email_id
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = sub

    msg.attach(MIMEText(msg_txt))
    #import pdb; pdb.set_trace();
    for f in attach or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    val = server.sendmail(email_id, email_id, msg.as_string())
    server.close()
    return val

if __name__=="__main__":
    send_mail("jnfsdkf", "hello", ["emotion_data_2017_06_09_19_34_11.png"])
