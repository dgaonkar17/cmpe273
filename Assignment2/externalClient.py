import grpc
import replicator_pb2

class myTest():
    def __init__(self, host='0.0.0.0', port=3000):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)

    def put(self, key, data):
        return self.stub.put(replicator_pb2.Request(key=key, data=data))

    def delete(self, key):
        return self.stub.delete(replicator_pb2.Request(key=key))

def main():
    test = myTest()
    response = test.put('Merry', 'Christmas')
    print(response.data)
    response = test.delete('Merry')
    print(response.data)


if __name__ == "__main__":
    main()


