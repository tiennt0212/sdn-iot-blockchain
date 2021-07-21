import sawtooth_sdk
from sawtooth_signing import create_context #use for create Private key and Signer
from sawtooth_signing import CryptoFactory #use for create Private key and Signer

import cbor #use for Encoding Payload

from hashlib import sha512
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader #use for create the Transaction Header
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction #use for create the Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader #use for create the Batch Header
from sawtooth_sdk.protobuf.batch_pb2 import Batch #use for create the Batch
from sawtooth_sdk.protobuf.batch_pb2 import BatchList #use for encode Batch in order to submit Batch to Validator.

import urllib.request #use for submit Batches to the Validator via Rest API
from urllib.error import HTTPError #use to get Error when submit.

#create Private key and Signer
context = create_context('secp256k1')
private_key = context.new_random_private_key()
signer = CryptoFactory(context).new_signer(private_key)

#Encoding Payload
payload = {
	'Verb': 'set',
	'Name': 'foo',
	'Value': 42}
payload_bytes = cbor.dumps(payload) #b'\xa3bTohEveryonegMessagelHello World!dFromjThanh Tien'
#This payload will be hashed to have a digest that will be located in txn_header


#Building the Transaction
###1.Transaction Header
txn_header_bytes = TransactionHeader(
	family_name='intkey',
	family_version='1.0',

	inputs=['1cf1266e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7'],
	outputs=['1cf1266e282c41be5e4254d8820772c5518a2c5a8c0c7f7eda19594a7eb539453e1ed7'],
    

	#batcher_public_key same as signer_public_key ~ signing the transaction with the same private key when signing the batch.
	signer_public_key=signer.get_public_key().as_hex(),
	batcher_public_key=signer.get_public_key().as_hex(), 

	# dependencies is a list of previous transaction header signatures
	# For example,
	# dependencies=['540a6803971d1880ec73a96cb97815a95d374cbad5d865925e5aa0432fcf1931539afe10310c122c5eaae15df61236079abbf4f258889359c4d175516934484a'],
	dependencies=[], 

	payload_sha512=sha512(payload_bytes).hexdigest()
).SerializeToString()

###2.Transaction
signature = signer.sign(txn_header_bytes) #integrity for txn_header.
txn = Transaction(
	header=txn_header_bytes,
	header_signature=signature,
	payload=payload_bytes
)


#IMPORTANT: Once you have one or more Transaction instances ready, they must be wrapped in a Batch.
#Batches are the atomic unit of change in Sawtooth’s state.
#When a Batch is submitted to a validator each Transaction in it will be applied (in order),
#or no Transactions will be applied.
#Even if your Transactions are not dependent on any others
#they cannot be submitted directly to the validator.
#They must all be wrapped in a Batch.


#Building the Batch
###1.Create the BatchHeader
txns = [txn] #txns is a list of transaction

batch_header_bytes = BatchHeader(
    signer_public_key=signer.get_public_key().as_hex(), #this public key also used in Transaction Header
    transaction_ids=[txn.header_signature for txn in txns], #is a list of ID = header_signature of every Transaction
).SerializeToString()

###2.Create the Batch
signature = signer.sign(batch_header_bytes) #integrity for batch_header
batch = Batch(
    header=batch_header_bytes,
    header_signature=signature,
    transactions=txns
)
###3.Encode the Batch(es) in a BatchList
#Only serialize to string, in order to submit batch(es) to Validator.
print(batch)
batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
print(batch_list_bytes)

#Submitting Batches to the Validator
try:
    request = urllib.request.Request(
        'http://127.0.0.1:8008/batches',
        batch_list_bytes,
        method='POST',
        headers={'Content-Type': 'application/octet-stream'})
    response = urllib.request.urlopen(request)

except HTTPError as e:
    response = e.file

print (response)



