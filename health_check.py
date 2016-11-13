import smtplib
import requests

def smtp_setup():
    
    msg = "Hey, check the site it might be down"
    from_addr = "fitbikeco101@hotmail.com"
    to_addrs = "fitbikeco101@hotmail.com"
    server = smtplib.SMTP('smtp.live.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("fitbikeco101@hotmail.com", "jessie")
    server.sendmail(from_addr, to_addrs, msg)
    server.quit()

    return server
        
def check_site(smtp_setup):
    requests.get("http://keepingupwithcass.hopto.org")
    status = requests.Response.ok 
    if not status:
        smtp_setup()

if __name__ == "__main__":
    check_site(smtp_setup)

    