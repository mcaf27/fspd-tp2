import sys
import threading
import grpc
import int_pb2, int_pb2_grpc
from concurrent import futures

class IntegrationServer(int_pb2_grpc.IntegrationServiceServicer):
    
    def __init__(self, stop_event):
        self.data = {} # dados indexados pelas chaves
        self._stop_event = stop_event
    
    def Registro(self, request, context):
        try:
            name = request.nome
            port = request.porto
            keys = request.chaves

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
            # o primeiro diretório que contém a chave é retornado
            name = self.data[key][0]['name']
            port = self.data[key][0]['port']

            return int_pb2.QueryResponse(nome=name, porto=port)
        else:
            return int_pb2.QueryResponse(nome='ND', porto=0)    

    def Termino(self, request, context):
        self._stop_event.set()
        return int_pb2.EndResponse(num=len(self.data))
    
def serve(port):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    int_pb2_grpc.add_IntegrationServiceServicer_to_server(IntegrationServer(stop_event), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    stop_event.wait()
    server.stop(2)

if __name__ == '__main__':
    serve(sys.argv[1])