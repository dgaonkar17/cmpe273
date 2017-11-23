import time
import grpc
import replicator_pb2
import replicator_pb2_grpc
import queue
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyReplicator(replicator_pb2.ReplicatorServicer):
    def __init__(self):
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))
        self.myqueue = queue.Queue()

    def replicate_on_slave(func):
        def func_wrapper(self, request, context):
            cmd = replicator_pb2.syncResponse(
                    cmd=func.__name__,
                    key=request.key.encode(),
                    val=request.val.encode()
                 ) 
            self.operations_queue.put(cmd)
            return func(self, request, context)
        return func_wrapper

    @replicate_on_slave
    def put(self, request, context):
        print("Puting {}:{} to master db".format(request.key, request.val))
        self.db.put(request.key.encode(), request.data.encode())
        return replicator_pb2.Response(data='ok')

    @replicate_on_slave
    def delete(self, request, context):
        print("Deleting {} from master db".format(request.key))
        self.db.delete(request.key.encode())
        return replicator_pb2.Response(data='ok')
   
    def sync(self, request, context):
        while True:
            command = self.myqueue.get()
            print("Sending operation ({}, {}, {}) to slave".format(command.cmd, command.key, command.val))
            yield command

def run(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    replicator_pb2_grpc.add_ReplicatorServicer_to_server(MyReplicator(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)



