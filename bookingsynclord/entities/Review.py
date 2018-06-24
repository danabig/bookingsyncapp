from Entity import Entity
class Review(Entity):
    """Represent a Review element.

    Documentation : http://developers.reviewsync.com/reference/endpoints/reviews/
    """
    ENTITY_TYPE = "reviews"
    def __init__(self,id = None):
        return super(Review,self).__init__("reviews",id)
