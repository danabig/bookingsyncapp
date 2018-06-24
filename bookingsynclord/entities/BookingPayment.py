from Entity import Entity
class BookingPayment(Entity):
    """Represent a BookingPayment element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/bookings_payments/
    """
    ENTITY_TYPE = "bookings_payments"
    def __init__(self,id = None):
        return super(BookingPayment,self).__init__("bookings_payments",id)
