# Runs protoc to generate protobuf messages and gRPC stubs.

from grpc_tools import protoc

protoc.main((
    '',
    '-I.',
    '--python_out=./airbloc/',
    '--grpc_python_out=./airbloc/',
    './proto/producer.proto'
))
print('Codes are generated into airbloc/proto.')
