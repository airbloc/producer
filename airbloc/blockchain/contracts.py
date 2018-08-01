import os
import json
from web3 import Web3
from web3.contract import ConciseContract


def _load_json_from(path):
    with open(path, mode='r') as file:
        return json.loads(file.read())


class Contracts:
    """ Wrapper class for managing contracts. """

    def __init__(self, deployment_path: str, abi_path: str, provider_uri: [str] = None):
        self._abi_path = abi_path

        if provider_uri:
            # override environment variables
            os.environ['WEB3_PROVIDER_URI'] = provider_uri

        self._contracts = {}
        self._deployments = _load_json_from(deployment_path)
        self._w3 = Web3()

    def get(self, name: str) -> ConciseContract:
        """ Returns interface of given contract. 
        :raises AssertionError if contract is defined in deploy.json 
        :raises FileNotFoundError if contract ABI is not found
        """
        if name in self._contracts:
            return self._contracts[name]

        # get deployed address
        if name not in self._deployments:
            raise AssertionError('Contract {} is not found in deploy.json file!'.format(name))
        address = self._deployments[name]

        # search ABI
        abi_path = os.path.join(self._abi_path, '{}.abi.json'.format(name))
        contract_abi = _load_json_from(abi_path)

        contract_instance = self._w3.eth.contract(address=address,
                                                  abi=contract_abi,
                                                  ContractFactoryClass=ConciseContract)
        self._contracts[name] = contract_instance
        return contract_instance
