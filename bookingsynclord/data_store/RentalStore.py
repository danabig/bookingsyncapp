from GenericStore import GenericStore

class RentalStore(GenericStore):
    """Store used to manage Rentals entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rentals/
    """
    def __init__(self,credential_manager):
        super(RentalStore, self).__init__(credential_manager,"rentals")
