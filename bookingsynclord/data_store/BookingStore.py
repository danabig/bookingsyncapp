from GenericStore import GenericStore
from bookingsynclord.entities.Booking import Booking
class BookingStore(GenericStore):
    """Store used to manage Bookings entities.

    http://developers.bookingsync.com/reference/endpoints/bookings/
    """

    def __init__(self,credential_manager):
        super(BookingStore, self).__init__(credential_manager,"bookings")

    def create_unavailable_booking(self,rental_id,start,end):
        """Create a new Booking entity representing an unavailability period
        on a rental.

        :param rental_id: ID of the rental which is unavailable
        :type  rental_id: string or integer
        :param start: start date of the unavailability period
        :type  start: datetime.datetime
        :param end  : end date of the unavailability period
        :type  end  : datetime.datetime
        :rtype       : entities.Booking
        """
        booking = Booking()
        booking.start_at = start.replace(microsecond=0).isoformat()
        booking.end_at = end.replace(microsecond=0).isoformat()
        booking.unavailable = True
        booking.rental_id = rental_id
        return booking
