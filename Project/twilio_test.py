from twilio.rest import Client

class twilio_test:
    # Your Account SID from twilio.com/console
    account_sid = "AC7e7981de6883ae957dc443a111206ff0"
    # Your Auth Token from twilio.com/console
    auth_token  = "d6cb557395c49e119d8e2e9f72cd5d07"
    client = Client(account_sid, auth_token)

    def send_msg(self,body,phone):

     message = self.client.messages.create(
     to=phone,
     from_="+18173811578",
     body=body
     # body="Hello from Python!"
         )
     print(message.sid)