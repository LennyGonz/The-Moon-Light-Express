# functions that will fetch the queries
import MySQLdb
import _mysql
import datetime
db = MySQLdb.connect("35.224.16.194","carlos","carlos","railroad1")
cursor = db.cursor()



def LookingReservation(location, destination):
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

    print(start_values, end_values)
    return start_values, end_values

def direction(startId,endId):
    if(startId < endId):
        return 1
    else:
        return 0

def MF(year,month,day):
    weekday=datetime.date(year,month,day).weekday()
    if(weekday== 5):
        day =1
    elif(weekday == 6):
        day =1
    else:
        day=0
    return day

def trains(direction,day):
    train_id_list = []
    cursor.execute("""select train_id from trains where train_days = %s and train_direction = %s""" , (day,direction))
    data = cursor.fetchall()
    for row in data:
        train_id_list.append(row[0])
    print(train_id_list)
    return train_id_list

#def Totalfare(seg1,seg2,type):


LookingReservation('Boston, MA - South Station','Stamford, CT')
trains(0,1)