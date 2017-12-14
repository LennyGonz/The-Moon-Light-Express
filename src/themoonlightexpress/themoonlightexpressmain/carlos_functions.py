# functions that will fetch the queries
# import MySQLdb
# import _mysql
import datetime
from django.db import connection, transaction

# db = MySQLdb.connect("35.224.16.194", "carlos", "carlos", "railroad1")
cursor = connection.cursor()

#pre:user input location and destination
#post: gets the station_id and symbol
def getstaion(location, destination):
<<<<<<<<< Temporary merge branch 1
    cursor.execute("""select station_id from stations where station_name= %s""" , [location])
=========
    # get train_id, segment_id
    cursor.execute("""select station_id from stations where station_name= %s""", [location])
>>>>>>>>> Temporary merge branch 2
    startid = cursor.fetchone()
    cursor.execute("""select station_symbol from stations where station_name=%s""", [location])
    startsymbol = cursor.fetchone()
    cursor.execute("""select station_id from stations where station_name=%s""", [destination])
    endid = cursor.fetchone()
    cursor.execute("""select station_symbol from stations where station_name=%s""", [destination])
    endsymbol = cursor.fetchone()
    start_values = []
    end_values = []
    for row in startid, startsymbol:
        start_values.append(row[0])
<<<<<<<<< Temporary merge branch 1
=========
        # start_values.insert(1,row[0])
>>>>>>>>> Temporary merge branch 2
    for row in endid, endsymbol:
        end_values.append(row[0])
    return start_values, end_values

<<<<<<<<< Temporary merge branch 1
#pre:takes the station_id for both location
#post: returns 0 for northbound, 1 for southbound
def direction(startId,endId):
    if(startId < endId):
=========

def direction(startId, endId):
    if (startId < endId):
>>>>>>>>> Temporary merge branch 2
        return 1
    else:
        return 0

<<<<<<<<< Temporary merge branch 1
#pre:takes a date in format year-month-day
#post: returns 0 for M-F and 1 for Sat-Sun-Holiday
=========

>>>>>>>>> Temporary merge branch 2
def MF(date1):
    data = date1.split("-")
    year = int(data[0])
    month = int(data[1])
    day = int(data[2])
    weekday = datetime.date(year, month, day).weekday()
    if (weekday == 5):
        day = 1
    elif (weekday == 6):
        day = 1
    else:
        day = 0
    return day

<<<<<<<<< Temporary merge branch 1
#pre: give direction and day of the week
#post: returns a list of train_id base on the direction and day
def trainsavible(direction,day):
=========

def trainsavible(direction, day):
>>>>>>>>> Temporary merge branch 2
    train_id_list = []
    cursor.execute("""select train_id from trains where train_days = %s and train_direction = %s""", (day, direction))
    data = cursor.fetchall()
    for row in data:
        train_id_list.append(row[0])
    #print(train_id_list)
    return train_id_list

<<<<<<<<< Temporary merge branch 1
#pre:gets list of segments, and fare type
#post: outputs the total fare
def Totalfare(segid,type):
=========

def Totalfare(segid, type):
>>>>>>>>> Temporary merge branch 2
    fare = 0
    rate = 0
    total = 0
    for id in segid:
        cursor.execute("""select seg_fare from segments WHERE segment_id = %s""", [id])
        row = cursor.fetchone()
        fare = fare + row[0]
    cursor.execute("""select rate from fare_types WHERE fare_name = %s""", [type])
    row1 = cursor.fetchone()
    rate = row1[0]
    total = rate + fare
    #print(total)
    return total

#pre:gets all of the information(comes from user)
#post:insert into the table reservation
def reservation(date,passengerid,card,billing):
    cursor.execute("insert into reservations" 
                   "(reservation_date, paying_passenger_id, card_number, billing_address)" 
                    "VALUES (%s,%s,%s,%s)",[date,passengerid,card,billing])
    db.commit()
#pre: gets all of the information
#post:insert into table passenger
def passenger(first,last,email,password,card,billing):
    cursor.execute("insert into passengers"
                   "(fname, lname, email, password, preferred_card_number, preferred_billing_address)"
                   "VALUES (%s,%s,%s,%s,%s,%s)", [first,last,email,password,card,billing])
    db.commit()

#pre: gets all information
#post:insert in table trips
def trips(date,startseg,endseg,type,fare,trainid,reservationid):
    cursor.execute("insert into trips"
                   "(trip_date, trip_seg_start, trip_seg_ends, fare_type, fare, trip_train_id, reservation_id)"
                   "VALUES (%s,%s,%s,%s,%s,%s,%s)", [date,startseg,endseg,type,fare,trainid,reservationid])
    db.commit()
#use function to grap the values from the return
#some of them are given by the user as they are inputting it.

#pre:give the train_id
#post:return a list of schedule base on the train
def schedule(id):
    timeline=[]
    for i in range(1,25):
        cursor.execute("""select station_id,time_in, time_out from stops_at WHERE train_id = %s""", [id] )
        row1 = cursor.fetchall()
        for row in row1:
            timeline.append(str(row[0]))
            timeline.append(str(row[1]))
            timeline.append(str(row[2]))
    return timeline


print(schedule(2))

<<<<<<<<< Temporary merge branch 1
#it works
print(getstaion('Boston, MA - South Station','Stamford, CT'))
print(trainsavible(0,1))
print(MF("2017-12-12"))
print(Totalfare((1,2,3,4,5),"adult"))
#reservation("2017-2-13",1,"544765434546","NY")
#passenger("rohan","swaby","lol@gmail.com","1235","654325543","BRONX")
=========
getstaion('Boston, MA - South Station', 'Stamford, CT')
trainsavible(0, 1)
print(MF("2017-12-12"))
Totalfare((1, 2, 3, 4, 5), "adult")
>>>>>>>>> Temporary merge branch 2
