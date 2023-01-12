from datetime import timedelta
from datetime import datetime
from datetime import time
import smtplib
from smtplib import SMTP
from email.message import EmailMessage
from okta_trust_client import OktaTrustClient
import sys

class OktaTrustEvent:

    def __init__(self, username, password) -> None:
        trust_client = OktaTrustClient()
        print(password)

        self.email_recipient = ['brandon.maranan@gmail.com','cipherbrm@gmail.com']
        self.credentials = {'username':username,'password':password}
        self.contents = trust_client.get_okta_trust_event()

    """
    Format message and returns both text and html message format
    """
    def format_message(self):

        text = f'**** UPDATED AS OF : {self.contents["updated"]} *******\n\n'
        for event in self.contents["okta_events"]:
            text += f'Title : {event["title"]}\n'
            text += f'Updated : {event["updated"]}\n'

            for content in event["contents"]:
                text += f'Summary : {content["value"]}\n'
            
            for link in event["links"]:
                text += f'Click on this link for details : {link["href"]}'
            
            text += "\n\n"
        

        html = f"""
        <html><body><center>
        <h1>Okta Status as of {self.contents["updated"]}</h1>
        """
        for content in event["contents"]:
            html += f"""
            <p>Summary: {content["value"]}</p>
            """
        
        html += """
        </center>
        </body>
        </html>
        """

        return {'text': text, 'html': html}

    """
    Send email to defined recipients
    """
    def send_email(self, format_type):
        print(format_type)
        msg = EmailMessage()

        msg['Subject'] = "Okta Trust Events"
        msg['From'] = self.credentials['username']
        msg['To'] = ','.join(self.email_recipient)

        print(self.credentials['username'])
        msg_body = self.format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['text'], subtype='html')
        with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
            server.starttls()
            server.login(self.credentials['username'],self.credentials['password'])
            server.send_message(msg)
    
    def test_self(me):
        print(me.format_message())


    
def test_send_email_success():
    assert True

def test_send_email_fail():
    assert False

if __name__ == "__main__":

    # date_time_str = '2023-01-06T16:03:34.693Z'
    # # strptime(input_string, input_format)
    # date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f%z')

    # print('Date-time:', date_time_obj)
    # rss_time = date_time_obj.timestamp(); 
    # print("RSS Time updated: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rss_time)))
    # print("RSS Time updated: " + time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(rss_time)))


    # currentTime = datetime.astimezone(datetime.now(), pytz.UTC).timestamp()
    # print(str(currentTime))

    # current_time_stamp = datetime.now().timestamp()
    # print(current_time_stamp)

    # my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentTime))
    # print("My current UTC from EPOCH " + my_time)

    # my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time_stamp))
    # print("My current Local time from EPOCH " + my_time)
    
    
    # my_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_time_stamp))
    # print("My current Local time from EPOCH " + my_time)
    
    # # timedelta.min()
    # struct_time = time.gmtime()
    # formatted_time = time.asctime(struct_time)
    # print(formatted_time)


    # last_update_in_minutes = (current_time_stamp - rss_time) / 60
    # print(str(last_update_in_minutes))
    # delta = 

    args = len(sys.argv)
    for arg in sys.argv:
        print(arg)

    if args == 3:
        email_sender = sys.argv[1]
        sender_password = sys.argv[2]
    else:
        print("Missing argument - Sender email and password is required ")
        exit()

    # password = input("Enter Email Sender password : ")

    if email_sender != ""  and sender_password != "":
        trust_event = OktaTrustEvent(email_sender, sender_password)
        trust_event.send_email("text")

        # test texrt
        print(trust_event.test_self())
        test_content = trust_event.format_message()
        if test_content:
            print(test_content['text'])
    else:
        print("Password is required")

    exit()