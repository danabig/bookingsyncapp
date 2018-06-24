from GenericStore import GenericStore

class BookingPaymentStore(GenericStore):
    """Store used to manage BookingStore entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/bookings_payments/
    """
    def __init__(self,credential_manager):
        super(BookingPaymentStore, self).__init__(credential_manager,"bookings_payments")
