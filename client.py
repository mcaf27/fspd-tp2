import sys
import grpc
import dir_pb2, dir_pb2_grpc

def run(addr):
    channel = grpc.insecure_channel(addr)
    stub = dir_pb2_grpc.DirectoryServiceStub(channel)

    while True:
        command_str = sys.stdin.readline().strip()
        if not command_str:
            break
        
        command = command_str.split(',')

        type = command[0]

        if type == 'I':
            chave = int(command[1])
            desc = command[2]
            valor = float(command[3])
            response = stub.Inserir(dir_pb2.InsertRequest(chave=chave, desc=desc, valor=valor))
            print(response.status)

        elif type == 'C':
            chave = int(command[1])
            response = stub.Consulta(dir_pb2.QueryRequest(chave=chave))
            
            desc = response.desc
            valor = float(response.valor)
            if desc == '' and valor == 0:
                print('-1')
            else:
                print(f'{desc},{valor:7.4f}')

        elif type == 'R':
            pass
        elif type == 'T':
            response = stub.Termino(dir_pb2.EmptyRequest())
            print(response.num)
            break

    channel.close()

if __name__ == '__main__':
    run(sys.argv[1])