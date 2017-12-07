import database
import random
import grpc
import datastore_pb2

PORT=3000

class Demo:
    def __init__(self):
        self.conn = database.connectToDB()

    def checkVacancy(self, roomtype, noofrooms):
        count = 0
        if roomtype == 'basic':
            count1 = database.checkAvailabliltyDB(self.conn, 1, 10 )
        elif roomtype == 'deluxe':
            count1 = database.checkAvailabliltyDB(self.conn, 11, 20)
        elif roomtype == 'premium':
            count1 = database.checkAvailabliltyDB(self.conn, 21, 30 )
        print(type(noofrooms))
        if((10-count1) >= int(noofrooms)):
            return True
        else:
            return False

    def getBookingDetails(self, bookingID):
        str1 = ""
        str2 = ""
        check_if_id_exists=database.checkBookingNo(self.conn, bookingID)
        if (bookingID != None and (check_if_id_exists)):
            rooms, details = database.getDetails(self.conn, bookingID)
            for x in rooms:
                str1 = str1 + " " + str(x[0])
            print(details)
            return "Here are your booking details: \n"+"Room numbers: " +str1 + "\n You checking date, price, room type: " + details

    #cancel room booking
    def cancelRoomBooking(self, bookingID):
        check_if_id_exists= database.checkBookingNo(self.conn, int(bookingID))
        if (bookingID != None and (database.checkBookingNo(self.conn,bookingID))):
            resp = database.cancelBooking(self.conn, bookingID)

            try:
                if (resp):
                    client = DatastoreClient(host='10.0.0.198')
                    cname = 'a'
                    phno = 'b'
                    cindate = 'c'
                    days = 'd'
                    roomtype = 'e'
                    price = 'f'
                    bookedroomlist = 'g'
                    optype = 'delete'
                    resp = client.put(str(bookingID), cname, phno, cindate, days,
                                      roomtype, price, bookedroomlist, optype)
                    key = resp.data
                    # print('RESPONSE: ' + key)
            except Exception as e:
                print(e)
            return "You booking under booking id "+ str(bookingID)  +" cancelled! We are refunding your money."
    # def getPhno(self,bookingID):

     #store room numbers in room table
    def storeRoomResponse(self, no_of_rooms, bookingID, limit_min, limit_max):
            # generate random no
            list1 = []
            while (no_of_rooms > 0):
                randomno = random.randint(limit_min, limit_max)
                if database.checkRoomNo(self.conn, randomno):
                    database.storeRoom(self.conn, randomno, bookingID)
                    list1.append(randomno)
                    no_of_rooms -= 1
            return list1

    #store user deatils in userdata
    def confirmBooking(self, roomtype, noofrooms, cindate,days, cname,phno,price, limit_min, limit_max):
        bookingId = database.storeSentResponse(self.conn, roomtype, cindate,int(days),cname,phno,price)
        bookedroomlist = self.storeRoomResponse(int(noofrooms), bookingId, limit_min, limit_max)
        stmt ="Done! Here are your booking details: \n" +"Booking id: "+str(bookingId)+ "\n"+"The bill comes to: "+str(price)
        try:
            if (bookedroomlist):
                optype = 'insert'
                client = DatastoreClient(host='10.0.0.198')
                resp = client.put(str(bookingId), str(cname), str(phno), str(cindate), str(days), str(roomtype),
                                  str(price), str(bookedroomlist), str(optype))
                key = resp.data
                print('RESPONSE: ' + key)
        except Exception as e:
            print(e)
        return  stmt, bookedroomlist


class DatastoreClient():
    def __init__(self, host='10.0.0.198', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def put(self, bid, uname, phno, cindate, days, rtype, price, rno, oprtyp):
        return self.stub.put(
            datastore_pb2.Request(bookingid=bid, username=uname, phoneno=phno, checkindate=cindate, noofdays=days,
                                  roomtype=rtype, price=price, roomno=rno, oprtype=oprtyp))
