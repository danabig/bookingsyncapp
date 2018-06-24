from GenericStore import GenericStore

class BookingFeeStore(GenericStore):
    """Store used to manage BookingFee entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/sources/
    """
    def __init__(self,credential_manager):
        super(BookingFeeStore, self).__init__(credential_manager,"bookings_fees")
