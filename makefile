stubs:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dir.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. int.proto

clean:
	rm -rf __pycache__
	rm -f *_pb2.py
	rm -f *_pb2_grpc.py

run_serv_dir:
	python3 server.py $(arg)

run_cli_dir:
	python3 client.py $(arg)

run_serv_int:
	python3 int_server.py $(arg)

run_cli_int:
	python3 int_client.py $(arg)