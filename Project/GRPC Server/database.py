import pymysql
import time
from datetime import datetime
from config import Config

def connectToDB():
    try:
        myConnection = pymysql.connect(host=Config.host, user=Config.user, passwd=Config.password,
                                       db=Config.db)
    except Exception as ex:
        myConnection = "error"
    return myConnection

def closeDbConnection(conn):
    conn.close()

def getAllRooms(conn):
    cur = conn.cursor()
    sql = "SELECT roomno FROM  Room_Association;"
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    return result

# To get responses from Database based on question
def getDetails(conn, bookingid):
    # log.writetofile("Sending query to DB")
    cur = conn.cursor()
    cur1 = conn.cursor()
    # sql1 = "SELECT * FROM userdata where bookingid = '%d'" %bookingid
    # cur.execute(sql1)
    sql = "SELECT roomno FROM Room_Association where bookingid = '%d'" % bookingid
    sql1 = "SELECT checkindate, roomtype, price FROM userdata where bookingid = '%d'" %bookingid
    cur1.execute(sql1)
    cur.execute(sql)
    result1 = cur.fetchall()
   # result1 = ', '.join([str(x) for x in result])
    result = cur1.fetchone()
    result2 = ', '.join([str(x) for x in result])
    return result1, result2

def storeSentResponse(conn, roomtype,cindate,days,cname,phno,price):
    # log.writetofile("storing sent response to DB..")
    now = datetime.now()
    now.strftime('%m/%d/%Y')
    cur = conn.cursor()
    bookid = 10
    insertstmt = "insert into userdata (username,phoneno,checkindate,noofdays,roomtype,price) values ('%s','%s','%s','%d','%s', '%d')" % (
        cname, phno, cindate, days, roomtype, price)
    cur.execute(insertstmt)
    timestamp = datetime.now()
    sentResponseID = conn.insert_id()
    conn.commit()
    return sentResponseID

def storeSentResponserep(conn,bid, roomtype,cindate,days,cname,phno,price):
    # log.writetofile("storing sent response to DB..")
    now = datetime.now()
    now.strftime('%m/%d/%Y')
    cur = conn.cursor()
    bookid = 10
    insertstmt = "insert into userdata (bookingid,username,phoneno,checkindate,noofdays,roomtype,price) values ('%d','%s','%s','%s','%d','%s', '%d')" % (
        bid,cname, phno, cindate, days, roomtype, price)
    cur.execute(insertstmt)
    timestamp = datetime.now()
    sentResponseID = conn.insert_id()
    conn.commit()
    return sentResponseID


def storeRoom(conn, bookid,roomno):
    insertstmt = "insert into Room_Association (bookingid,roomno) values ('%d', '%d')" % (
            bookid, roomno)
    cur = conn.cursor()
    cur.execute(insertstmt)

    sentResponseID = conn.insert_id()

    conn.commit()

def cancelBooking(conn, bookid):
    deletestmt1 = "delete from userdata where bookingid = '%d'" %bookid
    deletestmt2 = "delete from Room_Association where bookingid = '%d'" %bookid
    cur = conn.cursor()
    cur.execute(deletestmt1)
    cur.execute(deletestmt2)
    conn.commit()
    return True

def cancelBookingrep(conn, bookid):
    deletestmt1 = "delete from userdata where bookingid = '%d'" %bookid
    deletestmt2 = "delete from Room_Association where bookingid = '%d'" %bookid
    cur = conn.cursor()
    cur.execute(deletestmt1)
    cur.execute(deletestmt2)
    conn.commit()
    return True


def checkBookingNo(conn, bookid):
    cur = conn.cursor()
    sql = "SELECT bookingid FROM  userdata where bookingid = '%d'" %bookid
    rows_count = cur.execute(sql)
    if rows_count > 0:
        return True
    else:
        return False

def checkRoomNo(conn, roomno):
    cur = conn.cursor()
    sql = "SELECT bookingid FROM  Room_Association where roomno = '%d'" %roomno
    rows_count = cur.execute(sql)
    print(rows_count)
    if rows_count > 0:
        return False
    else:
        return True


def checkAvailabliltyDB(conn, x, y):
    cur = conn.cursor()
    sql = "SELECT * FROM Room_Association WHERE roomno BETWEEN '%d' AND '%d'" %(x, y);
    rows_count = cur.execute(sql)
    print(int(rows_count))
    return int(rows_count)