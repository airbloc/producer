import grpc
import json
import time
from airbloc.proto import RawData, Identifier, producer_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = producer_pb2_grpc.ProducerStub(channel)

identifier = Identifier(type='gaid', identifier='deadbeef-ff25-a091-1cd89bdabc79')
payload = json.dumps({
    'installedApps': [
        {
            'packageName': 'com.airbloc.test1',
            'installedAt': 1503202033
        },
        {
            'package': 'com.airbloc.test2',
            'installedAt': 1503202033
        },
    ]
})

data = RawData(categoryOfApp='installed-apps', ownerIdentifier=identifier, payload=payload)

def data_stream(given_data):
    for i in range(1):
        yield given_data
        time.sleep(0.5)

for result in stub.AddData(data_stream(data)):
    print('Inserted ID: {}'.format(result.dataId))
