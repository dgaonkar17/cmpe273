import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
from concurrent import futures
import database
import re
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.conn = database.connectToDB()


    def put(self, request, context):
        print("put")
        bid=request.bookingid
        uname=request.username
        phno=request.phoneno
        cindate=request.checkindate
        days=request.noofdays
        rtype=request.roomtype
        amt=request.price
        rno=request.roomno
        roomslist=re.findall(r'\d+', rno)
        oprtype=request.oprtype
        if(str(oprtype)=='insert'):
            resdb=database.storeSentResponserep(self.conn,int(bid),rtype,cindate,int(days),uname,phno,int(amt))
            for i in roomslist:
                xy=int(i)
                database.storeRoom(self.conn,int(bid ),int(xy))
            print("Replication Insert Done")
        elif(str(oprtype)=='delete'):
            database.cancelBooking(self.conn,int(bid))
            print("Replication Delete Done")
        return datastore_pb2.Response(data='received')

    def get(self, request, context):
        print("get")
        return datastore_pb2.Response(data='received')

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('10.0.0.198', 3000)
