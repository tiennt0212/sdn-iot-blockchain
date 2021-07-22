import traceback
import sys
import hashlib
import logging
import tokenlib

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

LOGGER = logging.getLogger(__name__)

FAMILY_NAME = "oceansong"
manager = tokenlib.TokenManager(secret="OCEANSONG")
def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

def _valid_token(token):
    try:
        manager.parse_token(token)
        return True
    except:
        return False

# Prefix for simplewallet is the first six hex digits of SHA-512(TF name).
sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

class SimpleWalletTransactionHandler(TransactionHandler):
    '''                                                       
    Transaction Processor class for the OCEANSONG transaction family.       
                                                              
    This with the validator using the accept/get/set functions.
    It implements functions to REGISTER and APPLY rules for any devices.
    '''

    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        '''This implements the apply function for this transaction handler.
                                                              
           This function does most of the work for this class by processing
           a single transaction for the OCEANSONG transaction family.   
        '''                                                   
        # Unpack transaction
        # Get the payload and extract information.
        header = transaction.header
        payload_list = transaction.payload.decode().split(",")
        command = payload_list[0]
        token = payload_list[1]
        info = payload_list[2]

        # Get the public key sent from the client.
        from_key = header.signer_public_key

        # Perform the command.
        LOGGER.info("Command = "+ command)

        if command == "register":
            self._register_token(context, token, from_key)
        else:
            LOGGER.info("Unhandled action. " +
                "Command should be register or transfer data")

    def _register_token(self, context, token, from_key):
        gateway_address = self._get_gateway_address(from_key)
        LOGGER.info('Got the key {} and the gateway address {} '.format(
            from_key, gateway_address))
        current_entry = context.get_state([gateway_address])

        if current_entry == []:
            LOGGER.info('No previous Gateway, creating new Gateway {} '
                .format(from_key))
            #Make a new token list
            tokenList = []
            
            # newtoken = int(id)rejected due to state root hash mismatch
        else:
            tokenList = current_entry[0].data.decode('utf-8')

        #Add a new token to tokenList
        tokenList.append(token)

        #Store data to BlockChain
        state_data = str(tokenList).encode('utf-8')
        addresses = context.set_state({gateway_address: state_data})

        if len(addresses) < 1:
            raise InternalError("State Error")

    def _get_gateway_address(self, from_key):
        return _hash(FAMILY_NAME.encode('utf-8'))[0:6] + _hash(from_key.encode('utf-8'))[0:64]



def setup_loggers():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

def main():
    '''Entry-point function for the simplewallet transaction processor.'''
    setup_loggers()
    try:
        # Register the transaction handler and start it.
        processor = TransactionProcessor(url='tcp://localhost:4004')

        handler = SimpleWalletTransactionHandler(sw_namespace)

        processor.add_handler(handler)

        processor.start()

    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

