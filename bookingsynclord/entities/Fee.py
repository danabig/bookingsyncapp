from Entity import Entity
class Fee(Entity):
    ENTITY_TYPE = "fees"
    """Represent a Fee element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/fees/
    """
    def __init__(self,id = None):
        return super(Fee,self).__init__("fees",id)
