from abc import ABCMeta
import simplejson as json
import copy
class Entity:
    """Abstract class with common properties for all entities."""
    __metaclass__ = ABCMeta

    def __init__(self, entity_type, id = None):
        # String Unique identifier (at this moment values are integers; may be replaced by GUIDs in future)
        self.id = id
        self.entity_type = entity_type

    def key_mapping(self):
        """Return attributes in dictionnary format
        :rtype: Dict
        """
        return self.__dict__

    def _to_json(self):
        """Return json serialization of Entity.
        :rtype: <string:representation of entity in json>
        """
        to_serialize = copy.deepcopy(self.__dict__)
        if to_serialize["id"] == None:
            to_serialize.pop("id")
        return to_serialize

    def _to_json_list(self):
        """Return json serialization of Entity.
        :rtype: <string:representation of entity in json>
        """
        to_serialize = copy.deepcopy(self.__dict__)
        if to_serialize["id"] == None:
            to_serialize.pop("id")
        to_serialize.pop("entity_type")
        list_to_serialize = { self.entity_type : [to_serialize] }
        return list_to_serialize

    def load_from_json(self,json):
        """Set attributes of an Entity by import JSON
        object received from API Call.

        :param json: loaded json
        :type  json: dictionnary
        """

        for key in json:
            setattr(self, key, json[key])

    def __str__(self):
        return(json.dumps(self._to_json(), indent=4, sort_keys=True))
