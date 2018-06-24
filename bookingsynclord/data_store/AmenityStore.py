from GenericStore import GenericStore


class AmenityStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/amenities/
    """
    def __init__(self,credential_manager):
        super(AmenityStore, self).__init__(credential_manager, "amenities")
