from GenericStore import GenericStore

class RentalFeeStore(GenericStore):
    """Store used to manage RentalFee entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rentals_fees/
    """
    def __init__(self,credential_manager):
        super(RentalFeeStore, self).__init__(credential_manager,"rentals_fees")
