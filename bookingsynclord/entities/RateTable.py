from Entity import Entity
class RateTable(Entity):
    ENTITY_TYPE = "rates_tables"
    """Represent a Rate Table element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rates_tables/
    """
    def __init__(self,id = None):
        return super(RateTable,self).__init__("rates_tables",id)
