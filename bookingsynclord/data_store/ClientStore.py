from GenericStore import GenericStore

class ClientStore(GenericStore):
    """Store used to manage BookingFee entities.

    BookingSync doc :     Documentation : http://developers.bookingsync.com/reference/endpoints/clients/
    """
    def __init__(self,credential_manager):
        super(ClientStore, self).__init__(credential_manager,"clients")
