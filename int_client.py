import sys
import grpc
import int_pb2, int_pb2_grpc
import dir_pb2, dir_pb2_grpc

def run(server_addr):
    channel = grpc.insecure_channel(server_addr)
    stub = int_pb2_grpc.IntegrationServiceStub(channel)

    while True:
        command_str = sys.stdin.readline().strip()
        if not command_str:
            break
        
        command = command_str.split(',')

        type_ = command[0]

        if type_ == 'C':
            chave = int(command[1])
            response = stub.Consulta(int_pb2.QueryRequest(chave=chave))
            nome = response.nome
            porto = response.porto

            if nome == 'ND':
                print('ND')
            else:
                # busca o valor no diretório especificado
                dir_addr = f'{nome}:{porto}'
                channel = grpc.insecure_channel(dir_addr)
                stub_dir = dir_pb2_grpc.DirectoryServiceStub(channel)
                response = stub_dir.Consulta(dir_pb2.QueryRequest(chave=chave))
                channel.close()
                print(f'{response.valor:7.4f}')

        elif type_ == 'T':
            response = stub.Termino(int_pb2.EmptyRequest())
            print(response.num)
            break

    channel.close()

if __name__ == '__main__':
    run(sys.argv[1])