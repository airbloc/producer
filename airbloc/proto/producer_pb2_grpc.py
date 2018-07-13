# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import producer_pb2 as producer__pb2


class ProducerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AddData = channel.stream_unary(
        '/Producer/AddData',
        request_serializer=producer__pb2.RawData.SerializeToString,
        response_deserializer=producer__pb2.AddDataSummary.FromString,
        )


class ProducerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def AddData(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProducerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AddData': grpc.stream_unary_rpc_method_handler(
          servicer.AddData,
          request_deserializer=producer__pb2.RawData.FromString,
          response_serializer=producer__pb2.AddDataSummary.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Producer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
