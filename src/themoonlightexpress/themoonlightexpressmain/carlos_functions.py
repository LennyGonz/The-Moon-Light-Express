# functions that will fetch the queries
# import MySQLdb
# import _mysql
import datetime
from django.db import connection, transaction

# db = MySQLdb.connect("35.224.16.194", "carlos", "carlos", "railroad1")
cursor = connection.cursor()


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
        # start_values.insert(1,row[0])
    for row in endid, endsymbol:
        end_values.append(row[0])

    print(start_values, end_values)
    return start_values, end_values


def direction(startId, endId):
    if (startId < endId):
        return 1
    else:
        return 0


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


def trainsavible(direction, day):
    train_id_list = []
    cursor.execute("""select train_id from trains where train_days = %s and train_direction = %s""", (day, direction))
    data = cursor.fetchall()
    for row in data:
        train_id_list.append(row[0])
    print(train_id_list)
    return train_id_list


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
    print(total)
    return total


getstaion('Boston, MA - South Station', 'Stamford, CT')
trainsavible(0, 1)
print(MF("2017-12-12"))
Totalfare((1, 2, 3, 4, 5), "adult")
