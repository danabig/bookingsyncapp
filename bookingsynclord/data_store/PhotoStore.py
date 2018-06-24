from GenericStore import GenericStore


class PhotoStore(GenericStore):
    """Store used to manage Photo entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/photos/
    """

    def __init__(self, credential_manager):
        super(PhotoStore, self).__init__(credential_manager, "photos")
