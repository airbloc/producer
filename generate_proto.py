# Runs protoc to generate protobuf messages and gRPC stubs.

from grpc_tools import protoc

protoc.main((
    '',
    '-I./protos',
    '--python_out=./airbloc/proto/',
    '--grpc_python_out=./airbloc/proto/',
    './protos/producer.proto'
))
