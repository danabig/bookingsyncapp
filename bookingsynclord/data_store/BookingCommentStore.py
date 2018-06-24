from GenericStore import GenericStore

class BookingCommentStore(GenericStore):
    """Store used to manage Source entities.

    BookingSync doc : http://developers.bookingsync.com/reference/endpoints/sources/
    """
    def __init__(self,credential_manager):
        super(BookingCommentStore, self).__init__(credential_manager,"booking_comments")
