from GenericStore import GenericStore

class PeriodStore(GenericStore):
    """Store used to manage Period entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/periods/
    """
    def __init__(self,credential_manager):
        super(PeriodStore, self).__init__(credential_manager,"periods")
