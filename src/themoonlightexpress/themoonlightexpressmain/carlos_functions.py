# functions that will fetch the queries
import MySQLdb
import _mysql
import datetime
db = MySQLdb.connect("35.224.16.194","carlos","carlos","railroad1")
cursor = db.cursor()



def getstaion(location, destination):
    #get train_id, segment_id
    cursor.execute("""select station_id from stations where station_name= %s""" , [location])
    startid = cursor.fetchone()
    cursor.execute("""select station_symbol from stations where station_name=%s""" , [location])
    startsymbol = cursor.fetchone()
    cursor.execute("""select station_id from stations where station_name=%s""",[destination])
    endid = cursor.fetchone()
    cursor.execute("""select station_symbol from stations where station_name=%s""" , [destination])
    endsymbol = cursor.fetchone()
    start_values=[]
    end_values=[]
    for row in startid, startsymbol:
        start_values.append(row[0])
        #start_values.insert(1,row[0])
    for row in endid, endsymbol:
        end_values.append(row[0])

    #print(start_values, end_values)
    return start_values, end_values

def direction(startId,endId):
    if(startId < endId):
        return 1
    else:
        return 0

def MF(date1):
    data = date1.split("-")
    year = int(data[0])
    month = int(data[1])
    day = int(data[2])
    weekday=datetime.date(year,month,day).weekday()
    if(weekday== 5):
        day =1
    elif(weekday == 6):
        day =1
    else:
        day=0
    return day

def trainsavible(direction,day):
    train_id_list = []
    cursor.execute("""select train_id from trains where train_days = %s and train_direction = %s""" , (day,direction))
    data = cursor.fetchall()
    for row in data:
        train_id_list.append(row[0])
    #print(train_id_list)
    return train_id_list

def Totalfare(segid,type):
    fare = 0
    rate = 0
    total= 0
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

def reservation(date,passengerid,card,billing):
    cursor.execute("insert into reservations" 
                   "(reservation_date, paying_passenger_id, card_number, billing_address)" 
                    "VALUES (%s,%s,%s,%s)",[date,passengerid,card,billing])
    db.commit()

def passenger(first,last,email,password,card,billing):
    cursor.execute("insert into passengers"
                   "(fname, lname, email, password, preferred_card_number, preferred_billing_address)"
                   "VALUES (%s,%s,%s,%s,%s,%s)", [first,last,email,password,card,billing])
    db.commit()

##make function to update the trips
def trips(date,startseg,endseg,type,fare,trainid,reservationid):
    cursor.execute("insert into trips"
                   "(trip_date, trip_seg_start, trip_seg_ends, fare_type, fare, trip_train_id, reservation_id)"
                   "VALUES (%s,%s,%s,%s,%s,%s,%s)", [date,startseg,endseg,type,fare,trainid,reservationid])
    db.commit()
#use function to grap the values from the return
#some of them are given by the user as they are inputting it.

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

#it works
print(getstaion('Boston, MA - South Station','Stamford, CT'))
print(trainsavible(0,1))
print(MF("2017-12-12"))
print(Totalfare((1,2,3,4,5),"adult"))
#reservation("2017-2-13",1,"544765434546","NY")
#passenger("rohan","swaby","lol@gmail.com","1235","654325543","BRONX")