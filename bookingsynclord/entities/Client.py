from Entity import Entity
class Client(Entity):
    """Represent a Client element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/clients/
    """
    ENTITY_TYPE = "clients"
    def __init__(self,id = None):
        return super(Client,self).__init__("clients",id)

