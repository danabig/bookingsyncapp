from GenericStore import GenericStore

class SourceStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/sources/
    """
    def __init__(self,credential_manager):
        super(SourceStore, self).__init__(credential_manager,"sources")
