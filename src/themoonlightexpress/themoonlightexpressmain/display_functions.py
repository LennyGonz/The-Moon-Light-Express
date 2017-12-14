import MySQLdb
#from .models import SeatsFree
db = MySQLdb.connect("35.224.16.194","miguel","miguel","railroad1")
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
    cursor.execute("""select * from reservations where paying_passenger_id= %s""", [pass_id]) #query
    reservations = cursor.fetchall() #fetch all reservations related to that passenger

    return reservations

def can_reserve(train_id,segment_id):
    """Check if there are available seats for that train and segment
            Parameters
            ----------
            train_id: train to be taken
            segment_id: segment at start station

            Returns
            -------
            boolean for reservation (T or F)
            """
    cursor.execute("""select freeseat from seats_free where train_id= %s and segment_id= %s""", [train_id,segment_id])  # query
    available_seats = cursor.fetchone()  # fetch all reservations related to that passenger
    print(available_seats)
    if available_seats[0] == 448:
        return False;
    return True;

def decrement_seats(train_id, segments):
    """Decrease a seat for train_id for list of segments
                Parameters
                ----------
                train_id: train
                segments: list of segments id's

                """
    for segment in segments:
        #Probably will need date as well to update FreeSeats
        cursor.execute("""update seats_free set freeseat = freeseat - 1 
                        where train_id = %s and segment_id = %s""",[train_id,segment])
        db.commit()


#print(get_pass_reservations(1))
#print(can_reserve(1,1))
print('IMHERE')
#print(decrement_seats(1,[1,2])) #probably need the date as well