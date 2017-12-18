import MySQLdb

# from .models import SeatsFree
db = MySQLdb.connect("35.224.16.194", "miguel", "miguel", "railroad1")
cursor = db.cursor()


def get_pass_reservations(pass_id):
    """Get all passenger reservations.
        Parameters
        ----------
        pass_id: passenger_id

        Returns
        -------
        reservations : list of reservations
        """
    cursor.execute("""select * from reservations where paying_passenger_id= %s""", [pass_id])  # query
    reservations = cursor.fetchall()  # fetch all reservations related to that passenger

    return reservations


def can_reserve(train_id, segment_id, date):
    """Check if there are available seats for that train and segment
            Parameters
            ----------
            train_id: train to be taken
            segment_id: segment at start station

            Returns
            -------
            boolean for reservation (T or F)
            """
    segments=[]
    for seg in segment_id:
        cursor.execute("""select freeseat from seats_free where train_id= %s and segment_id= %s and seat_free_date = %s""",
                   [train_id, seg,date])  # query
        available_seats = cursor.fetchone()  # fetch all reservations related to that passenger
        segments.append(available_seats[0])
    #print(segments)
    for i in segments:
        if i < 0:
            return False
        else:
            return True





def decrement_seats(train_id, segments, date):
    """Decrease a seat for train_id for list of segments
                Parameters
                ----------
                train_id: train
                segments: list of segments id's

                """
    for seg in segments:
        # Probably will need date as well to update FreeSeats
        cursor.execute("""update seats_free set freeseat = freeseat - 1 
                        where train_id = %s and segment_id = %s and seat_free_date = %s""", [train_id, seg, date])
        db.commit()


#print(get_pass_reservations(1))
#print(can_reserve(1,[1,2,3,4],"2017-12-13"))
#print('IMHERE')
#decrement_seats(1,[1,2,3,4],"2017-11-13") #probably need the date as well
