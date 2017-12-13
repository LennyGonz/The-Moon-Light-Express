import MySQLdb

db = MySQLdb.connect("35.224.16.194", "adi", "adi", "railroad1")
cursor = db.cursor()



def get_segments(location_id, destination_id):
    segments = []
    if(location_id < destination_id):
        for i in range(location_id, destination_id):
            cursor.execute("SELECT segment_id from segments where seg_n_end ="
                 "%s and seg_s_end = %s", (location_id, location_id + 1))
            row = cursor.fetchone()
            segments.append(row[0])
            location_id += 1
    else:
        x = location_id
        y = destination_id
        for i in range(y, x):
            cursor.execute("SELECT segment_id from segments where seg_n_end ="
                               "%s and seg_s_end = %s", (y, y + 1))
            row = cursor.fetchone()
            segments.append(row[0])
            y += 1
    return segments


def get_avail_trains_free_seats(train_id, segment_id, date):
    train_id_list = []
    for i in range(0, len(train_id)):
        free_seats = []
        for j in range(0, len(segment_id)):
            cursor.execute("SELECT freeseat from seats_free where train_id = "
                       "%s and segment_id = %s and seat_free_date = %s", [train_id[i], segment_id[j], date])
            row = cursor.fetchone()
            free_seats.append(row[0])
            j+=1
        l = 0
        for k in range(0, len(free_seats)):
            if free_seats[k] == 0:
                l += 1
            k+=1

        if l == 0:
            train_id_list.append(train_id[i])
        i+=1
    return train_id_list

def get_time(train_id, location, destination):
    for i in range(0, len(train_id)):
        mylist = []
        cursor.execute("SELECT time_in, time_out from stops_at WHERE train_id = %s and "
                       "station_id = %s", (train_id[i], location))
        row = cursor.fetchone()
        mylist.append(str(row[0]))
        mylist.append(str(row[1]))
        cursor.execute("SELECT time_in, time_out from stops_at WHERE train_id = %s and "
                       "station_id = %s", (train_id[i], destination))
        row = cursor.fetchone()
        mylist.append(str(row[0]))
        mylist.append(str(row[1]))
        return mylist




cursor.close()
db.close()