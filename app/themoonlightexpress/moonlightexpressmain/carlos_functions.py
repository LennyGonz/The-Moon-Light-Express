# functions that will fetch the queries
import MySQLdb
import _mysql
import datetime

from app.themoonlightexpress.moonlightexpressmain.adi_functions import *
from app.themoonlightexpress.moonlightexpressmain.display_functions import *


db = MySQLdb.connect("35.224.16.194", "carlos", "carlos", "railroad1")
cursor = db.cursor()


# pre:user input location and destination
# post: gets the station_id and symbol
def getstaion(location, destination):
    # get train_id, segment_id
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
        start_values.append(row[0])
    for row in endid, endsymbol:
        end_values.append(row[0])
    return start_values, end_values


# pre:takes the station_id for both location
# post: returns 0 for northbound, 1 for southbound
def direction(startId, endId):
    if (startId < endId):
        return 0
    else:
        return 1


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
    train_id_list = []
    cursor.execute("""select train_id from trains where train_days = %s and train_direction = %s""", (day, direction))
    data = cursor.fetchall()
    for row in data:
        train_id_list.append(row[0])
    return train_id_list


# pre:gets list of segments, and fare type
# post: outputs the total fare
def Totalfare(segid, type):
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
    return total


# pre:gets all of the information(comes from user)
# post:insert into the table reservation
def reservation(date, passengerid, card, billing):
    cursor.execute("insert into reservations"
                   "(reservation_date, paying_passenger_id, card_number, billing_address)"
                   "VALUES (%s,%s,%s,%s)", [date, passengerid, card, billing])
    db.commit()


# pre: gets all of the information
# post:insert into table passenger
def passenger(first, last, email, card, billing):
    cursor.execute("insert into passengers"
                   "(fname, lname, email, preferred_card_number, preferred_billing_address)"
                   "VALUES (%s,%s,%s,%s,%s,%s)", [first, last, email, card, billing])
    db.commit()


# pre: gets all information
# post:insert in table trips
def trips(date, startseg, endseg, type, fare, trainid, reservationid):
    cursor.execute("insert into trips"
                   "(trip_date, trip_seg_start, trip_seg_ends, fare_type, fare, trip_train_id, reservation_id)"
                   "VALUES (%s,%s,%s,%s,%s,%s,%s)", [date, startseg, endseg, type, fare, trainid, reservationid])
    db.commit()


# use function to grap the values from the return
# some of them are given by the user as they are inputting it.

# pre:give the train_id
# post:return a list of schedule base on the train
def schedule(id):
    timeline = []
    for i in range(1, 25):
        cursor.execute("""select station_id,time_in, time_out from stops_at WHERE train_id = %s""", [id])
        row1 = cursor.fetchall()
        for row in row1:
            timeline.append(str(row[0]))
            timeline.append(str(row[1]))
            timeline.append(str(row[2]))
    return timeline


# pre:put all function together
# post:reservation process

def ChoosingTrain(location, destination, date, faretype):
    # variables
    start = []
    end = []
    start, end = getstaion(location, destination)
    startid = start[0]
    startsym = start[1]
    endid = end[0]
    endsym = end[1]

    # functions
    northorsouth = direction(startid, endid)
    segmentlist = get_segments(startid, endid)
    day = MF(date)
    listoftrain = trainsavible(northorsouth, day)
    for train in listoftrain:
        yes = can_reserve(train,segmentlist,date)
        if(yes != True):
            listoftrain.remove(train)
    i = [2, 4, 5, 10, 12, 13]
    for x in i:
        if x in listoftrain:
            listoftrain.remove(x)
    trainstochoose = get_avail_trains_free_seats(listoftrain, segmentlist, date)
    fare = int(Totalfare(segmentlist, faretype))
    startseg = startid
    endseg = endid
    timeschedule = train_and_time(trainstochoose, startseg, endseg)
    return fare, startseg, endseg, timeschedule


def expressTrain(location, destination, date, faretype):
    # variables
    start = []
    end = []
    start, end = getstaion(location, destination)
    startid = start[0]
    startsym = start[1]
    endid = end[0]
    endsym = end[1]

    # functions
    northorsouth = direction(startid, endid)
    segmentlist = get_segments(startid, endid)
    day = MF(date)
    listoftrain = trainsavible(northorsouth, day)
    for train in listoftrain:
        yes = can_reserve(train,segmentlist,date)
        if(yes != True):
            listoftrain.remove(train)
    i = [1, 3, 6, 7, 8, 9,11,14, 15, 16, 17,18, 19,20,21, 22, 23, 24, 25, 26, 27, 28]
    for x in i:
        if x in listoftrain:
            listoftrain.remove(x)
    trainstochoose = get_avail_trains_free_seats(listoftrain, segmentlist, date)
    fare = int(Totalfare(segmentlist, faretype))
    fare = (fare * 1.02) + fare
    fare = float("{:.2f}".format(fare))
    startseg = startid
    endseg = endid
    timeschedule = train_and_time(trainstochoose, startseg, endseg)
    return fare, startseg, endseg, timeschedule



# pre:take a list of trainid, location, and destination
# post: return a list containing the id for each train with it's departure and arrival time
def train_and_time(train_id, location, destination):
    bigger_train_id_and_time = []
    my_bigger_list = get_time(train_id, location, destination)
    for i in range(0, len(train_id)):
        train_id_and_time = []
        train_id_and_time.append(train_id[i])
        train_id_and_time.append(my_bigger_list[i])
        bigger_train_id_and_time.append(train_id_and_time)
    return bigger_train_id_and_time


# pre: takes first name
# post: returns the passengerid and reservation id
def getid(fname):
    cursor.execute("""select passenger_id from passengers WHERE fname = %s""", [fname])
    name = cursor.fetchone()
    cursor.execute("""select reservation_id from reservations WHERE paying_passenger_id = %s""", [name])
    reservation = cursor.fetchone()
    return name[0], reservation[0]


# pre:takes all of the parameter
# post: insert into the passenger,trips,and reservation table
def Confirmation(train, fname, lname, email, cc, billing, date, fare, startseg, endseg, faretype):
    passenger(fname, lname, email, cc, billing)
    passid, reservationid = getid(fname)
    reservation(date, passid, cc, billing)
    trips(date, startseg, endseg, faretype, fare, train, reservationid)
    segments = range(startseg,endseg+1)
    decrement_seats(train,segments,date)


def Cancellation(reservation_id):
    cursor.execute("""delete from trips WHERE reservation_id = %s""",[reservation_id])
    db.commit()
    cursor.execute("""select paying_passenger_id from reservations WHERE reservation_id = %s""",[reservation_id])
    passid = cursor.fetchone()
    cursor.execute("""delete from reservations WHERE reservation_id = %s""",[reservation_id])
    db.commit()
    cursor.execute("""delete from passengers WHERE passenger_id = %s""",[passid[0]])
    db.commit()



#Cancellation(8)

print(ChoosingTrain('Boston, MA - South Station','New Rochelle, NY', "2018-01-10", "adult"))
print(expressTrain('Boston, MA - South Station','New Rochelle, NY', "2018-01-10", "adult"))


#
# #it works
# print(getstaion('Boston, MA - South Station','Stamford, CT'))
# print(trainsavible(0,1))
# print(MF("2017-12-12"))
# print(Totalfare((1,2,3,4,5),"adult"))
# #reservation("2017-2-13",1,"544765434546","NY")
# #passenger("rohan","swaby","lol@gmail.com","1235","654325543","BRONX")
#Confirmation("1","mike","gonzales","mike@gmail.com","5432543523","Astoria","2017-11-13",95,"1","12","adult")

cursor.close()
db.close()
