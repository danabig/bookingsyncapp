from GenericStore import GenericStore

class RateStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rates/
    """
    def __init__(self,credential_manager):
        super(RateStore, self).__init__(credential_manager,"rates")
