from GenericStore import GenericStore

class FeeStore(GenericStore):
    """Store used to manage Fee entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rentals_fees/
    """
    def __init__(self,credential_manager):
        super(FeeStore, self).__init__(credential_manager,"fees")
