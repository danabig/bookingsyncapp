from Entity import Entity
class Rate(Entity):
    ENTITY_TYPE = "rates"
    """Represent a Rental element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rates/
    """
    def __init__(self,id = None):
        return super(Rate,self).__init__("rates",id)
