from Entity import Entity
class Season(Entity):
    ENTITY_TYPE = "seasons"
    """Represent a Season element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/seasons/
    """
    def __init__(self,id = None):
        return super(Season,self).__init__("seasons",id)
