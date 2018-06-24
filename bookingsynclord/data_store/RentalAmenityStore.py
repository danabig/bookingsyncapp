from GenericStore import GenericStore


class RentalAmenityStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rentals_amenities/
    """
    def __init__(self,credential_manager):
        super(RentalAmenityStore, self).__init__(credential_manager, "rentals_amenities")
