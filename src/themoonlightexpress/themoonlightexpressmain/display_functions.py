import MySQLdb
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

def can_reserve(trip_id):
    """Get all passenger reservations.

            Parameters
            ----------
            pass_id: passenger_i

            Returns
            -------
            reserve_bool : boolean for reservation (T or F)
            """

print(get_pass_reservations(1))
print('IMHERE')
