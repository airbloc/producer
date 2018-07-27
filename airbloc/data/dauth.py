from airbloc.blockchain import Contracts

class DAuth:

    def __init__(self, contracts: Contracts):
        self.registry = contracts.get('DAuthRegistry')

    def is_allowed(self, user_aid: str, category_id: str) -> bool:
        """ Check DAuth registry on blockchain that user allowed data collection. """

        # TODO: decode user_aid to reach real user ID
        # TODO: match protocol with actual contract
        return self.registry.isAllowed(user_aid, category_id)
