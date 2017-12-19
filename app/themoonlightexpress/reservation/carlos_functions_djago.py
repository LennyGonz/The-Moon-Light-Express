# functions that will fetch the queries
# import MySQLdb
# import _mysql
import datetime
from django.db import connection, transaction
from .adi_functions_django import *
from .display_functions_dango import *

#pre:user input location and destination
# post: gets the station_id and symbol
def getstaion(location, destination):
    # get train_id, segment_id
    cursor = connection.cursor()
    cursor.execute("""select station_id from stations where station_name= %s""", [location])
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
        if row is not None:
            start_values.append(row[0])
    for row in endid, endsymbol:
        if row is not None:
            end_values.append(row[0])
    cursor.close()
    return start_values, end_values


# pre:takes the station_id for both location
# post: returns 0 for northbound, 1 for southbound
def direction(startId, endId):
    if (startId < endId):
        return 1
    else:
        return 0


# pre:takes a date in format year-month-day
# post: returns 0 for M-F and 1 for Sat-Sun-Holiday
def MF(date1):
    data = date1.split("-")
    year = int(data[0])
    month = int(data[1])
    day = int(data[2])
    weekday = datetime.date(year, month, day).weekday()
    if (weekday == 5):
        day = 0
    elif (weekday == 6):
        day = 0
    else:
        day = 1
    return day


# pre: give direction and day of the week
# post: returns a list of train_id base on the direction and day
def trainsavible(direction, day):
    cursor = connection.cursor()
    train_id_list = []
    cursor.execute("""select train_id from trains where train_days = %s and train_direction = %s""", (day, direction))
    data = cursor.fetchall()
    for row in data:
        train_id_list.append(row[0])
    cursor.close()
    return train_id_list


# pre:gets list of segments, and fare type
# post: outputs the total fare
def Totalfare(segid, type):
    cursor = connection.cursor()
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
    cursor.close()
    return total


# pre:gets all of the information(comes from user)
# post:insert into the table reservation
def reservation(date, passengerid, card, billing):
    cursor = connection.cursor()
    cursor.execute("insert into reservations"
                   "(reservation_date, paying_passenger_id, card_number, billing_address)"
                   "VALUES (%s,%s,%s,%s)", [date, passengerid, card, billing])
    transaction.commit()
    cursor.close()



# pre: gets all of the information
# post:insert into table passenger
def passenger(first, last, email, card, billing):
    cursor = connection.cursor()
    cursor.execute("insert into passengers"
                   "(fname, lname, email, preferred_card_number, preferred_billing_address)"
                   "VALUES (%s,%s,%s,%s,%s,%s)", [first, last, email, card, billing])
    transaction.commit()
    cursor.close()



# pre: gets all information
# post:insert in table trips
def trips(date, startseg, endseg, type, fare, trainid, reservationid):
    cursor = connection.cursor()
    cursor.execute("insert into trips"
                   "(trip_date, trip_seg_start, trip_seg_ends, fare_type, fare, trip_train_id, reservation_id)"
                   "VALUES (%s,%s,%s,%s,%s,%s,%s)", [date, startseg, endseg, type, fare, trainid, reservationid])
    transaction.commit()
    cursor.close()


# use function to grap the values from the return
# some of them are given by the user as they are inputting it.

# pre:give the train_id
# post:return a list of schedule base on the train
def schedule(id):
    cursor = connection.cursor()
    timeline = []
    for i in range(1, 25):
        cursor.execute("""select station_id,time_in, time_out from stops_at WHERE train_id = %s""", [id])
        row1 = cursor.fetchall()
        for row in row1:
            timeline.append(str(row[0]))
            timeline.append(str(row[1]))
            timeline.append(str(row[2]))
    cursor.close()
    return timeline


# pre:put all function together
# post:reservation process

def ChoosingTrain(location, destination, date, faretype):
    # variables
    start = []
    end = []
    #start, end = getstaion(location, destination)
    startid = int(location)
    endid = int(destination)

    # functions
    northorsouth = direction(startid, endid)
    segmentlist = get_segments(startid, endid)
    day = MF(date)
    listoftrain = trainsavible(northorsouth, day)
    #If this breaks the form this is the new thing i added, this checks for trains that have seat,
    #we pop the trainid that are full
    for train in listoftrain:
        yes = can_reserve(train,segmentlist,date)
        if(yes != True):
            listoftrain.remove(train)
    trainstochoose = get_avail_trains_free_seats(listoftrain, segmentlist, date)
    time = get_time(trainstochoose, startid, endid)
    fare = int(Totalfare(segmentlist, faretype))
    print("segmentlist",segmentlist)
    startseg = segmentlist[0]
    endseg = segmentlist[-1]
    timeschedule = train_and_time(trainstochoose, startseg, endseg)
    return fare, startseg, endseg, timeschedule


def train_and_time(train_id, location, destination):
    bigger_train_id_and_time = []
    my_bigger_list = get_time(train_id, location, destination)
    for i in range(0, len(train_id)):
        train_id_and_time = []
        train_id_and_time.append(train_id[i])
        train_id_and_time.append(my_bigger_list[i])
        bigger_train_id_and_time.append(train_id_and_time)
    return bigger_train_id_and_time


def getid(fname):
    cursor = connection.cursor()
    cursor.execute("""select passenger_id from passengers WHERE fname = %s""", [fname])
    name = cursor.fetchone()
    cursor.execute("""select reservation_id from reservations WHERE paying_passenger_id = %s""", [name])
    reservation = cursor.fetchone()
    cursor.close()
    return name[0], reservation[0]


def Confirmation(train, fname, lname, email, cc, billing, date, fare, startseg, endseg, faretype):
    passenger(fname, lname, email, cc, billing)
    passid, reservationid = getid(fname)
    reservation(date, passid, cc, billing)
    trips(date, startseg, endseg, faretype, fare, train, reservationid)
    #This is new too, couldnt test as a whole function but it works individually
    segments = range(startseg, endseg + 1)
    decrement_seats(train, segments, date)


# fare,startseg,endseg,trainsche = ChoosingTrain('Boston, MA - South Station', 'Stamford, CT', "2018-01-12", "adult")
# print(trainsche)

# print(schedule(2))
#
# #it works
# print(getstaion('Boston, MA - South Station','Stamford, CT'))
# print(trainsavible(0,1))
# print(MF("2017-12-12"))
# print(Totalfare((1,2,3,4,5),"adult"))
# #reservation("2017-2-13",1,"544765434546","NY")
##passenger("rohan","swaby","lol@gmail.com","1235","654325543","BRONX")