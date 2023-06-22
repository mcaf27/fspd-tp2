import sys
import grpc
import dir_pb2, dir_pb2_grpc

def run(server_addr):
    channel = grpc.insecure_channel(server_addr)
    stub = dir_pb2_grpc.DirectoryServiceStub(channel)

    while True:
        command_str = sys.stdin.readline().strip()
        if not command_str:
            break
        
        command = command_str.split(',')

        type_ = command[0]

        if type_ == 'I':
            chave = int(command[1])
            desc = command[2]
            valor = float(command[3])
            response = stub.Inserir(dir_pb2.InsertRequest(chave=chave, desc=desc, valor=valor))
            print(response.status)

        elif type_ == 'C':
            chave = int(command[1])
            response = stub.Consulta(dir_pb2.QueryRequest(chave=chave))
            
            desc = response.desc
            valor = float(response.valor)
            if desc == '' and valor == 0:
                print('-1')
            else:
                print(f'{desc},{valor:7.4f}')

        elif type_ == 'R':
            nome_serv_int = command[1]
            porto_serv_int = int(command[2])

            response = stub.Registro(dir_pb2.RegisterRequest(nome=nome_serv_int, porto=porto_serv_int))
            print(response.num)

        elif type_ == 'T':
            response = stub.Termino(dir_pb2.EmptyRequest())
            print(response.num)
            break

    channel.close()

if __name__ == '__main__':
    run(sys.argv[1])