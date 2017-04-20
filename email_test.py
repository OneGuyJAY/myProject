import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header

sender = 'julin.shan@autodesk.com'
receivers = ['jie.chen@autodesk.com']

# standard email
def email_temp1():
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    msg['Subject'] = 'Just a test'

    body = 'hello, just a test for python script'

    msg.attach(MIMEText(body, 'plain'))

    smtpObj = smtplib.SMTP('mail.o365.autodesk.com', timeout=120)
    try:
        text = msg.as_string()
        smtpObj.sendmail(sender, receivers, text)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
    finally:
        smtpObj.quit()

# very sample mail
def email_temp2():
    message = """From: From jie.chen@autodesk.com
    To: To jie.chen@autodesk.com
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """
    smtpObj = smtplib.SMTP('mail.o365.autodesk.com', timeout=120)
    try:
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
    finally:
        smtpObj.quit()

# attach file
def email_temp3():
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    msg['Subject'] = 'Just a test'

    body = 'hello buddy'
    msg.attach(MIMEText(body, 'plain'))
    att1 = MIMEText(open('D:/FeacsAutomation/Feacs_Fusion/Report_Feacs26/2017- 2-23.json', 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'  # unknown type
    att1["Content-Disposition"] = 'attachment; filename="test.json"'
    msg.attach(att1)

    smtpObj = smtplib.SMTP('mail.o365.autodesk.com', timeout=120)
    try:
        text = msg.as_string()
        smtpObj.sendmail(sender, receivers, text)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
    finally:
        smtpObj.quit()

# insert image into text
def email_temp4():
    msg = MIMEMultipart('related')  # insert something into email ("内嵌")
    msg['From'] = sender
    msg['To'] = ','.join(receivers)
    msg['Subject'] = 'Just a test'

    body = '''
    <p>Python testing...</p>
    <p><a href="http://www.baidu.com">123456</a></p>
    <p>img shows:</p>
    <p><img src="cid:image1"></p>
    '''
    # src="cid:image1"  means image insert in text

    # once some HyperText existed in body, we should add argument 'alternative'
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgAlternative.attach(MIMEText(body, 'html', 'utf-8'))

    # open image and attach into text
    fp = open('Image 27.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    smtpObj = smtplib.SMTP('mail.o365.autodesk.com', timeout=120)
    try:
        text = msg.as_string()
        smtpObj.sendmail(sender, receivers, text)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
    finally:
        smtpObj.quit()

if __name__ == '__main__':
    email_temp1()
