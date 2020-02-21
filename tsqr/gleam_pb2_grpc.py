# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import gleam_pb2 as gleam__pb2


class GleamMasterStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetResources = channel.unary_unary(
        '/pb.GleamMaster/GetResources',
        request_serializer=gleam__pb2.ComputeRequest.SerializeToString,
        response_deserializer=gleam__pb2.AllocationResult.FromString,
        )
    self.SendHeartbeat = channel.stream_unary(
        '/pb.GleamMaster/SendHeartbeat',
        request_serializer=gleam__pb2.Heartbeat.SerializeToString,
        response_deserializer=gleam__pb2.Empty.FromString,
        )
    self.SendFlowExecutionStatus = channel.stream_unary(
        '/pb.GleamMaster/SendFlowExecutionStatus',
        request_serializer=gleam__pb2.FlowExecutionStatus.SerializeToString,
        response_deserializer=gleam__pb2.Empty.FromString,
        )


class GleamMasterServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetResources(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendHeartbeat(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendFlowExecutionStatus(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GleamMasterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetResources': grpc.unary_unary_rpc_method_handler(
          servicer.GetResources,
          request_deserializer=gleam__pb2.ComputeRequest.FromString,
          response_serializer=gleam__pb2.AllocationResult.SerializeToString,
      ),
      'SendHeartbeat': grpc.stream_unary_rpc_method_handler(
          servicer.SendHeartbeat,
          request_deserializer=gleam__pb2.Heartbeat.FromString,
          response_serializer=gleam__pb2.Empty.SerializeToString,
      ),
      'SendFlowExecutionStatus': grpc.stream_unary_rpc_method_handler(
          servicer.SendFlowExecutionStatus,
          request_deserializer=gleam__pb2.FlowExecutionStatus.FromString,
          response_serializer=gleam__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'pb.GleamMaster', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class GleamExecutorStub(object):
  """////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CollectExecutionStatistics = channel.stream_unary(
        '/pb.GleamExecutor/CollectExecutionStatistics',
        request_serializer=gleam__pb2.ExecutionStat.SerializeToString,
        response_deserializer=gleam__pb2.Empty.FromString,
        )


class GleamExecutorServicer(object):
  """////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////

  """

  def CollectExecutionStatistics(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GleamExecutorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CollectExecutionStatistics': grpc.stream_unary_rpc_method_handler(
          servicer.CollectExecutionStatistics,
          request_deserializer=gleam__pb2.ExecutionStat.FromString,
          response_serializer=gleam__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'pb.GleamExecutor', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class GleamAgentStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SendFileResource = channel.stream_stream(
        '/pb.GleamAgent/SendFileResource',
        request_serializer=gleam__pb2.FileResourceRequest.SerializeToString,
        response_deserializer=gleam__pb2.FileResourceResponse.FromString,
        )
    self.Execute = channel.unary_stream(
        '/pb.GleamAgent/Execute',
        request_serializer=gleam__pb2.ExecutionRequest.SerializeToString,
        response_deserializer=gleam__pb2.ExecutionResponse.FromString,
        )
    self.CollectExecutionStatistics = channel.stream_unary(
        '/pb.GleamAgent/CollectExecutionStatistics',
        request_serializer=gleam__pb2.ExecutionStat.SerializeToString,
        response_deserializer=gleam__pb2.Empty.FromString,
        )
    self.Delete = channel.unary_unary(
        '/pb.GleamAgent/Delete',
        request_serializer=gleam__pb2.DeleteDatasetShardRequest.SerializeToString,
        response_deserializer=gleam__pb2.DeleteDatasetShardResponse.FromString,
        )
    self.Cleanup = channel.unary_unary(
        '/pb.GleamAgent/Cleanup',
        request_serializer=gleam__pb2.CleanupRequest.SerializeToString,
        response_deserializer=gleam__pb2.CleanupResponse.FromString,
        )
    self.AllocateDspCore = channel.unary_unary(
        '/pb.GleamAgent/AllocateDspCore',
        request_serializer=gleam__pb2.DspCoreRequest.SerializeToString,
        response_deserializer=gleam__pb2.DspCoreResponse.FromString,
        )
    self.AllocateDspPort = channel.unary_unary(
        '/pb.GleamAgent/AllocateDspPort',
        request_serializer=gleam__pb2.DspPortRequest.SerializeToString,
        response_deserializer=gleam__pb2.DspPortResponse.FromString,
        )
    self.ReleaseTaskGroupDspResources = channel.unary_unary(
        '/pb.GleamAgent/ReleaseTaskGroupDspResources',
        request_serializer=gleam__pb2.ReleaseTaskGroupDspResourcesRequest.SerializeToString,
        response_deserializer=gleam__pb2.Empty.FromString,
        )
    self.StartRemoteExecutor = channel.unary_unary(
        '/pb.GleamAgent/StartRemoteExecutor',
        request_serializer=gleam__pb2.StartDsp.SerializeToString,
        response_deserializer=gleam__pb2.Error.FromString,
        )
    self.StopRemoteExecutor = channel.unary_unary(
        '/pb.GleamAgent/StopRemoteExecutor',
        request_serializer=gleam__pb2.StopDsp.SerializeToString,
        response_deserializer=gleam__pb2.Error.FromString,
        )
    self.RemoteExecutorStats = channel.unary_unary(
        '/pb.GleamAgent/RemoteExecutorStats',
        request_serializer=gleam__pb2.GetDspStat.SerializeToString,
        response_deserializer=gleam__pb2.ExecutionStat.FromString,
        )
    self.SendFileToRemoteExecutor = channel.unary_unary(
        '/pb.GleamAgent/SendFileToRemoteExecutor',
        request_serializer=gleam__pb2.SendFile.SerializeToString,
        response_deserializer=gleam__pb2.Error.FromString,
        )


class GleamAgentServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SendFileResource(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Execute(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CollectExecutionStatistics(self, request_iterator, context):
    """collect execution stats from "gleam execute" processes
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Cleanup(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AllocateDspCore(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AllocateDspPort(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ReleaseTaskGroupDspResources(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StartRemoteExecutor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StopRemoteExecutor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoteExecutorStats(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendFileToRemoteExecutor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GleamAgentServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SendFileResource': grpc.stream_stream_rpc_method_handler(
          servicer.SendFileResource,
          request_deserializer=gleam__pb2.FileResourceRequest.FromString,
          response_serializer=gleam__pb2.FileResourceResponse.SerializeToString,
      ),
      'Execute': grpc.unary_stream_rpc_method_handler(
          servicer.Execute,
          request_deserializer=gleam__pb2.ExecutionRequest.FromString,
          response_serializer=gleam__pb2.ExecutionResponse.SerializeToString,
      ),
      'CollectExecutionStatistics': grpc.stream_unary_rpc_method_handler(
          servicer.CollectExecutionStatistics,
          request_deserializer=gleam__pb2.ExecutionStat.FromString,
          response_serializer=gleam__pb2.Empty.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=gleam__pb2.DeleteDatasetShardRequest.FromString,
          response_serializer=gleam__pb2.DeleteDatasetShardResponse.SerializeToString,
      ),
      'Cleanup': grpc.unary_unary_rpc_method_handler(
          servicer.Cleanup,
          request_deserializer=gleam__pb2.CleanupRequest.FromString,
          response_serializer=gleam__pb2.CleanupResponse.SerializeToString,
      ),
      'AllocateDspCore': grpc.unary_unary_rpc_method_handler(
          servicer.AllocateDspCore,
          request_deserializer=gleam__pb2.DspCoreRequest.FromString,
          response_serializer=gleam__pb2.DspCoreResponse.SerializeToString,
      ),
      'AllocateDspPort': grpc.unary_unary_rpc_method_handler(
          servicer.AllocateDspPort,
          request_deserializer=gleam__pb2.DspPortRequest.FromString,
          response_serializer=gleam__pb2.DspPortResponse.SerializeToString,
      ),
      'ReleaseTaskGroupDspResources': grpc.unary_unary_rpc_method_handler(
          servicer.ReleaseTaskGroupDspResources,
          request_deserializer=gleam__pb2.ReleaseTaskGroupDspResourcesRequest.FromString,
          response_serializer=gleam__pb2.Empty.SerializeToString,
      ),
      'StartRemoteExecutor': grpc.unary_unary_rpc_method_handler(
          servicer.StartRemoteExecutor,
          request_deserializer=gleam__pb2.StartDsp.FromString,
          response_serializer=gleam__pb2.Error.SerializeToString,
      ),
      'StopRemoteExecutor': grpc.unary_unary_rpc_method_handler(
          servicer.StopRemoteExecutor,
          request_deserializer=gleam__pb2.StopDsp.FromString,
          response_serializer=gleam__pb2.Error.SerializeToString,
      ),
      'RemoteExecutorStats': grpc.unary_unary_rpc_method_handler(
          servicer.RemoteExecutorStats,
          request_deserializer=gleam__pb2.GetDspStat.FromString,
          response_serializer=gleam__pb2.ExecutionStat.SerializeToString,
      ),
      'SendFileToRemoteExecutor': grpc.unary_unary_rpc_method_handler(
          servicer.SendFileToRemoteExecutor,
          request_deserializer=gleam__pb2.SendFile.FromString,
          response_serializer=gleam__pb2.Error.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'pb.GleamAgent', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))