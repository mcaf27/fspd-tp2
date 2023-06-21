import sys
import grpc
import dir_pb2, dir_pb2_grpc
from concurrent import futures

class DirectoryServer(dir_pb2_grpc.DirectoryServiceServicer):
    
    def __init__(self):
        self.directory = {}

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
        return dir_pb2.EndResponse(num=len(self.directory))
    
    def Registro(self, request, context):
        pass
    
def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dir_pb2_grpc.add_DirectoryServiceServicer_to_server(DirectoryServer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print('Server started!')
    server.wait_for_termination()

if __name__ == '__main__':
    serve(sys.argv[1])