from Entity import Entity
class Source(Entity):
    ENTITY_TYPE = "sources"
    """Represent a Rental element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rentals/
    """
    def __init__(self,id = None):
        return super(Source,self).__init__("sources",id)
