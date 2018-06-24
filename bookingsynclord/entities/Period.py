from Entity import Entity
class Period(Entity):
    ENTITY_TYPE = "periods"
    """Represent a Rental element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/periods/
    """
    def __init__(self,id = None):
        return super(Period,self).__init__("periods",id)
