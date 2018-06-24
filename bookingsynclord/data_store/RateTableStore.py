from GenericStore import GenericStore

class RateTableStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/rates_tables/
    """
    def __init__(self,credential_manager):
        super(RateTableStore, self).__init__(credential_manager,"rates_tables")
