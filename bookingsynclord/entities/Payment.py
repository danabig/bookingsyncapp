from Entity import Entity
class Payment(Entity):
    """Represent a Payment element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/payments/
    """
    ENTITY_TYPE = "payments"
    def __init__(self,id = None):
        return super(Payment, self).__init__("payments",id)

