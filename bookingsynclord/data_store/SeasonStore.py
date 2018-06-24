from GenericStore import GenericStore

class SeasonStore(GenericStore):
    """Store used to manage Season entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/seasons/
    """
    def __init__(self,credential_manager):
        super(SeasonStore, self).__init__(credential_manager,"seasons")
