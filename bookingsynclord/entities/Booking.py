from Entity import Entity
class Booking(Entity):
    """Represent a Booking element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/bookings/
    """
    ENTITY_TYPE = "bookings"
    def __init__(self,id = None):
        return super(Booking,self).__init__("bookings",id)
        self.start_at = None
        self.end_at = None
        self.unavailable = False
        self.adults = 0
        self.rental_id = 0
