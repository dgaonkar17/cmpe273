from twilio.rest import Client

class twilio_test:
    # Your Account SID from twilio.com/console
    account_sid = config.twilio_sid
    # Your Auth Token from twilio.com/console
    auth_token  = config.twilio_token
    client = Client(account_sid, auth_token)

    def send_msg(self,body,phone):

     message = self.client.messages.create(
     to=phone,
     from_="+18173811578",
     body=body
     # body="Hello from Python!"
         )
     print(message.sid)
