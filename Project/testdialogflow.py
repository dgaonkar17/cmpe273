
from __future__ import print_function

import os
import sys
import database
import json
import ConnectDB
from ConnectDB import Demo
from BookingVariables import BookingVariables
from twilio_test import twilio_test
from pprint import pprint
import slackclient, time
from yelp_handle import yelp_handle



try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )

    import apiai




CLIENT_ACCESS_TOKEN=config.dialogflow_token



VALET_SLACK_NAME = 'demobot'
VALET_SLACK_TOKEN = config.slack_token
VALET_SLACK_ID = config.slack_id
valet_slack_client = slackclient.SlackClient(VALET_SLACK_TOKEN)
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)


def call_yelp(result):
        print("hi yelp")
        # print("result" +result)
        # checks parameter value
        # param = result['contexts']
        param=result
        if param != []:
            res = param['parameters']
            if res != {}:  # if parameters values are present
                category = res['category']  # get no of rooms
                print(category)
                city=res['city']
                print(city)
                y_handle = yelp_handle()
                name,phno,url=y_handle.test_yelp(category,city)
                return name,phno,url
                # print(myval)



def checkVacancy(roomtype, noofrooms):
    demo = Demo()
    if demo.checkVacancy(roomtype, noofrooms):
        return True
    else:
        return False



def setBookingInfo(intentname,bvarobj, result,channel):
    print(intentname)
    if (intentname == 'roomdetails'):
        bvarobj.roomtype = getRoomType(result)
        bvarobj.noofrooms = getNoOfRooms(result)
        if checkVacancy(bvarobj.roomtype, bvarobj.noofrooms) == False :
            #reset class booking  variables
            bvarobj.roomtype = None
            bvarobj.noofrooms = None
            return "Not available , Please select different type of room."

    elif(intentname=='userdetails'):
        bvarobj.cindate=getCheckinDate(result)
    elif(intentname=='userdetails_noofdays'):
        bvarobj.days=getNoOfDays(result)
    elif(intentname=='userdetails_name'):
        bvarobj.cname=getCustomerName(result)
    elif(intentname=='userdetails_custom'):
        bvarobj.phno=getPhoneNo(result)
        return Booktheroom(bvarobj)
    elif(intentname == 'bookingdetails' or intentname == 'bookingdetails_new'):
        return getBookingDetails(result)
    elif intentname == 'cancellation':
        return cancelBooking(result)



def getBookingDetails(result):
    demo = Demo()
    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                booking_no = res['book_no']  # get no of rooms
                booking_resp= demo.getBookingDetails(int(booking_no))
                return booking_resp
    except Exception as e:
        print(str(e))

def getRoomType(result):
    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                room_type = res['room_type']  # get type of room
                return room_type.lower()

    except Exception as e:
        print(str(e))


def getNoOfRooms(result):

    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                no_of_rooms = res['no_of_rooms']  # get no of rooms
                return int(no_of_rooms)

    except Exception as e:
        print(str(e))

def getCheckinDate(result):

    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                checkin_date = res['checkin_date']  # get no of rooms
                return checkin_date

    except Exception as e:
        print(str(e))

def getNoOfDays(result):

    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                no_of_days = res['no_of_days']  # get no of rooms
                return no_of_days

    except Exception as e:
        print(str(e))

def getCustomerName(result):
    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                customer_name = res['customer_name']  # get no of rooms
                return customer_name

    except Exception as e:
        print(str(e))

def getPhoneNo(result):
    try:
        # checks parameter value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                phone_no = res['phone_no']  # get no of rooms
                return phone_no

    except Exception as e:
        print(str(e))




def Booktheroom(bvarobjcopy):
    demo = Demo()
    twi_test=twilio_test()
    price=0
    limit_min =0
    limit_max = 0
    if(bvarobjcopy.roomtype is not None and bvarobjcopy.noofrooms is not None and bvarobjcopy.cindate is not None and bvarobjcopy.days is not None and bvarobjcopy.cname is not None and bvarobjcopy.phno is not None):
        if(bvarobjcopy.roomtype=='deluxe'):
            price=int(bvarobjcopy.days) * (bvarobjcopy.noofrooms) * 1000
            limit_min = 11
            limit_max = 20
        elif(bvarobjcopy.roomtype=='premium'):
            price=int(bvarobjcopy.days) * (bvarobjcopy.noofrooms) * 1500
            limit_min = 21
            limit_max = 30
        elif (bvarobjcopy.roomtype == 'basic'):
            price = int(bvarobjcopy.days) * (bvarobjcopy.noofrooms) * 500
            limit_min = 1
            limit_max = 10

        responsebooked,bookinglist=demo.confirmBooking(bvarobjcopy.roomtype,bvarobjcopy.noofrooms,bvarobjcopy.cindate,bvarobjcopy.days,bvarobjcopy.cname,bvarobjcopy.phno,price, limit_min, limit_max)
        body=responsebooked + "\n Your rooms: " +str(bookinglist)+ "\n Have a wonderful stay at the Spartans Hotel."
        twi_test.send_msg(body,bvarobjcopy.phno)
        return responsebooked + "\n Your rooms: " +str(bookinglist)+ "\n Have a wonderful stay at the Spartans Hotel."

def cancelBooking(result):
    demo = Demo()
    twi_test = twilio_test()
    try:
        # checks parametebook r value
        param = result['contexts']
        if param != []:
            res = param[0]['parameters']
            if res != {}:  # if parameters values are present
                # phone_no = res['phone_no']  # get no of rooms
                booking_no = res['booking_no']  # get no of rooms
                cancel_resp = demo.cancelRoomBooking(int(booking_no))
                body=cancel_resp
                phoneno='+16692044653'
                twi_test.send_msg(body,phoneno)
                return cancel_resp

    except Exception as e:
        print(str(e))

def connectDialogflow(message, user, bvarobj,channel) :

        request = ai.text_request()
        request.query = message
        # print(json.loads(request.getresponse().read()))
        str=request.getresponse().read().decode('utf-8')
        response = json.loads(str)
        print(response)
        result = response['result']
        action = result.get('action')
        actionIncomplete = result.get('actionIncomplete', False)

        #intent name
        intentname = result['metadata']['intentName']

        if(intentname == 'food'):
            name, phno, url = call_yelp(result)
        # attachments =  { "attachments": [{"title": "",
        #                                "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/r1LTDXoRXMpv4TQ3Jy149Q/o.jpg"}]}
        # print(attachments)
        # valet_slack_client.api_call('chat.postEphemeral', channel=channel,text="",
        #                              attachment=attachments, as_user=True,unfurl_media=False)
            my_list =[name,phno,url]
        # if myval != None:


            return my_list

        booking_resp = setBookingInfo(intentname, bvarobj, result,channel)
        if booking_resp != None:
            return booking_resp
        else:
            return response['result']['fulfillment']['speech']


def get_mention(user):
    return '<@{user}>'.format(user=user)

valet_slack_mention = get_mention(VALET_SLACK_ID)


def is_for_me(event):
    """Know if the message is dedicated to me"""
    # check if not my own event
    type = event.get('type')
    if type and type == 'message' and not (event.get('user') == VALET_SLACK_ID):
        # in case it is a private message return true
        if is_private(event):
            return True
        # in case it is not a private message check mention
        text = event.get('text')
        channel = event.get('channel')
        if valet_slack_mention in text.strip().split():
            return True



def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')

def get_mention(user):
    return '<@{user}>'.format(user=user)

valet_slack_mention = get_mention(VALET_SLACK_ID)




def handle_message(message, user, channel, bvarobj):
    user_mention = get_mention(user)
    resp = connectDialogflow(message, user, bvarobj,channel )
    if (isinstance(resp,list)==True):
       for i in resp:
           valet_slack_client.api_call('chat.postMessage', channel=channel,
                                       text=i, as_user=True, unfurl_media=False)
    else:
        valet_slack_client.api_call('chat.postMessage', channel=channel,
                                    text=resp, as_user=True, unfurl_media=False)



def connectSlack(bvarobj):
    if valet_slack_client.rtm_connect():
        print('[.] Valet de Machin is ON...')
        while True:
            event_list = valet_slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    if is_for_me(event):
                        print(event)
                        handle_message(message=event.get('text'), user=event.get('user'),
                                           channel=event.get('channel'), bvarobj= bvarobj )
    else:
        print('[!] Connection to Slack failed.')

if __name__ == '__main__':
    bvarobj = BookingVariables()
    connectSlack(bvarobj)

