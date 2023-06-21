import sys
import grpc
import int_pb2, int_pb2_grpc
from concurrent import futures

class IntegrationServer(int_pb2_grpc.IntegrationServiceServicer):
    
    def __init__(self):
        self.data = {}
    
    def Registro(self, request, context):
        try:
            name = request.name
            port = request.port
            keys = request.keys

            for key in keys:
                if key in self.data:
                    self.data[key].append({ 'port': port, 'name': name })
                else:
                    self.data[key] = [{ 'port': port, 'name': name }]

            return int_pb2.RegisterResponse(num=len(keys))
        except:
            return int_pb2.RegisterResponse(num=0)
        
    def Consulta(self, request, context):
        key = request.chave

        if key in self.data:
            name = self.data[key][0]['name']
            port = self.data[key][0]['port']

            return int_pb2.QueryResponse(nome=name, porto=port)
        else:
            return int_pb2.QueryResponse(nome='ND', porto=0)    

    def Termino(self, request, context):
        return int_pb2.EndResponse(num=len(self.data))
    
def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    int_pb2_grpc.add_IntegrationServiceServicer_to_server(IntegrationServer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print('Server started!')
    server.wait_for_termination()

if __name__ == '__main__':
    serve(sys.argv[1])