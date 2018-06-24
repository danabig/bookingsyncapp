from GenericStore import GenericStore

class ReviewStore(GenericStore):
    """Store used to manage Review entities.

    BookingSync doc :     Documentation : http://developers.bookingsync.com/reference/endpoints/reviews/
    """
    def __init__(self,credential_manager):
        super(ReviewStore, self).__init__(credential_manager,"reviews")
