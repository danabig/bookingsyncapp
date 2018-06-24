from Entity import Entity
class RateRule(Entity):
    ENTITY_TYPE = "rates_rules"
    """Represent a Rental element.

    Documentation : http://developers.bookingsync.com/reference/endpoints/rates_rules/
    """
    def __init__(self,id = None):
        return super(RateRule,self).__init__("rates_rules",id)
