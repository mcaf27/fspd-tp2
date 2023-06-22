import sys
import threading
import grpc
import dir_pb2, dir_pb2_grpc
import int_pb2, int_pb2_grpc
from concurrent import futures
from socket import getfqdn

class DirectoryServer(dir_pb2_grpc.DirectoryServiceServicer):
    
    def __init__(self, port, stop_event):
        self.directory = {}
        self.port = port
        self._stop_event = stop_event

    def Inserir(self, request, context):

        status = int(request.chave in self.directory)
        
        self.directory[request.chave] = {
            'desc': request.desc,
            'valor': request.valor
        }

        return dir_pb2.InsertResponse(status=status)
    
    def Consulta(self, request, context):
        if request.chave in self.directory:
            desc = self.directory[request.chave]['desc']
            val = self.directory[request.chave]['valor']
            return dir_pb2.QueryResponse(desc=desc, valor=val)
        else:
            return dir_pb2.QueryResponse(desc='', valor=0)
        
    def Termino(self, request, context):
        self._stop_event.set()
        return dir_pb2.EndResponse(num=len(self.directory))
    
    def Registro(self, request, context):
        name_int = request.nome
        port_int = request.porto
        keys = list(self.directory.keys())
        server_name = getfqdn()

        # faz uma conexão com o serviço de integração
        int_addr = f'{name_int}:{port_int}'
        channel = grpc.insecure_channel(int_addr)
        stub = int_pb2_grpc.IntegrationServiceStub(channel)

        request = int_pb2.RegisterRequest()
        request.nome = server_name
        request.porto = int(self.port)
        request.chaves.extend(keys)

        response = stub.Registro(request)

        channel.close()

        return dir_pb2.RegisterResponse(num=response.num)
    
def serve(port):
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dir_pb2_grpc.add_DirectoryServiceServicer_to_server(DirectoryServer(port, stop_event), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    stop_event.wait()
    server.stop(2)

if __name__ == '__main__':
    serve(sys.argv[1])