import grpc
import replicator_pb2
import rocksdb

class doReplication():
    def __init__(self, host='0.0.0.0', port=3000):
        self.db = rocksdb.DB("slave.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)

    def sync(self):
        syncAll = self.stub.sync(replicator_pb2.syncRequest())
        for op in syncAll:
            if op.op == 'put':
                print("Putting {}:{} to slave db".format(op.key, op.data))
                self.db.put(op.key.encode(), op.data.encode())
            elif op.op == 'delete':
                print("Deleting {} from slave db".format(op.key))
                self.db.delete(op.key.encode())

def run():
    slave = doReplication()
    response = slave.sync()

if __name__ == "__main__":
    run()

