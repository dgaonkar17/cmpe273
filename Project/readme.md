# CMPE 273 Project - Spartan Hotel Chatbot

The Spartan hotel chatbot is built for providing chat assistance to customers. This System is integrated to slack application which provides answer to the query of the customers. Customer can ask general queries through the bot such as room booking, booking details and cancellation. This bot provides easy access to our customers to chat with us and other assistance. The System has been trained using Dialogflow API to answer different queries. The System analyses the question and than answers to the user. The other exciting features such as weather information, SMS notification after booking / cancellations and nearby top ranked restaurants recommendations using YELP API.

## API suite: 
1. Dialogflow API
2. Python SDK integration to api.ai 
3. MySQL Database for storing the user and booking details.
4. Replication to multiple servers using GRPC for distributed system.
5. Weather script deployed on Heroku which is integrated to Dialogflow using webhook. 
6. Twilio service for SMS notification.
7. Yelp API to get top recommendations of nearby restaurants. 



### Room booking on Slackbot:

![Alt text](https://github.com/dgaonkar17/cmpe273/blob/master/Project/images/Booking_Slack.png)


### Notification sent to user when a booking is made by SMS using Twilio service:

![Alt text](https://github.com/dgaonkar17/cmpe273/blob/master/Project/images/booking_twilio.png)
