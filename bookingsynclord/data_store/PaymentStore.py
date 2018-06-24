from GenericStore import GenericStore

class PaymentStore(GenericStore):
    """Store used to manage BookingFee entities.

    BookingSync doc :     Documentation : http://developers.bookingsync.com/reference/endpoints/payments/
    """
    def __init__(self,credential_manager):
        super(PaymentStore, self).__init__(credential_manager, "payments")
