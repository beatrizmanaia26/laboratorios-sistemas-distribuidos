"""import grpc
import task_manager_pb2
import task_manager_pb2_grpc

def connection_test(stub):
    print("Testando conexão com servidor")
    request = task_manager_pb2.ConnRequest(message="SYN")
    response = stub.ConnectionTest(request)
    print(f"Resposta: {response}", flush=True)

def create_task(stub, title, description):
    request = task_manager_pb2.CreateRequest(title=title, description=description)
    response = stub.Create(request)
    print(f"Tarefa criada: {response}", flush=True)
    return response.id

def get_task(stub, id):
    request = task_manager_pb2.GetRequest(id=str(id))
    try:
        response = stub.Get(request)
        print(f"Tarefa: {response}", flush=True)
    except grpc.RpcError as e:
        print(e.details(), flush=True)

def list_tasks(stub):
    request = task_manager_pb2.ListRequest()
    response = stub.List(request)
    print("Lista de tarefas:", flush=True)
    for task in response.tasks:
        print(task, flush=True)

def update_task(stub, id, title, description, status):
    request = task_manager_pb2.UpdateRequest(id=str(id), title=title, description=description, status=status)
    try:
        response = stub.Update(request)
        print(f"Tarefa atualizada: {response}", flush=True)
    except grpc.RpcError as e:
        print(e.details(), flush=True)

def delete_task(stub, id):
    request = task_manager_pb2.DeleteRequest(id=str(id))
    try:
        stub.Delete(request)
        print("Tarefa apagada", flush=True)
    except grpc.RpcError as e:
        print(e.details(), flush=True)

print("Cliente conectando com o servidor",flush=True)
porta = "50051"
endereco = "servidor"
with grpc.insecure_channel(f"{endereco}:{porta}") as channel:
    stub = task_manager_pb2_grpc.TaskManagerStub(channel)
    connection_test(stub)

    create_task(stub, "teste", "teste de tarefa")
    get_task(stub, 1)
    list_tasks(stub)
    update_task(stub, 1, "atualizacao", "teste de update", "completa")
    list_tasks(stub)
    delete_task(stub, 1)
    list_tasks(stub)
"""
import json

import grpc
import task_manager_pb2
import task_manager_pb2_grpc
from google.protobuf.json_format import MessageToJson

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

print("Cliente conectando com o servidor",flush=True)
porta = "50051"
endereco = "servidor"
channel = grpc.insecure_channel(f"{endereco}:{porta}")
stub = task_manager_pb2_grpc.TaskManagerStub(channel)

print("Inicializando FastAPI", flush=True)
app = FastAPI()

class Tarefa(BaseModel):
    titulo: str
    descricao: str
    status: str

@app.get("/")
def list_tasks():
    request = task_manager_pb2.ListRequest()
    response = MessageToJson(stub.List(request))
    return JSONResponse(content=json.loads(response))

@app.get("/test")
def connection_test():
    print("Testando conexão com servidor")
    request = task_manager_pb2.ConnRequest(message="SYN")
    response = stub.ConnectionTest(request)
    return response.message

@app.put("/adicionar/")
def create_task(tarefa: Tarefa):
    request = task_manager_pb2.CreateRequest(
        title=tarefa.titulo,
        description=tarefa.descricao,
    )
    response = stub.Create(request)
    return response.id

@app.get("/tarefa/{pos}")
def get_task(id: int):
    request = task_manager_pb2.GetRequest(id=str(id))
    try:
        response = MessageToJson(stub.Get(request))
        return JSONResponse(content=json.loads(response))
    except grpc.RpcError as e:
        print(e.details(), flush=True)


@app.put("/atualizar/")
def update_task(tarefa: Tarefa, id: int):
    request = task_manager_pb2.UpdateRequest(
        id=str(id),
        title=tarefa.titulo,
        description=tarefa.descricao,
        status=tarefa.status
    )
    try:
        response = stub.Update(request)
        print(f"Tarefa atualizada: {response}", flush=True)
    except grpc.RpcError as e:
        print(e.details(), flush=True)

@app.delete("/deletar/{pos}")
def delete_task(id: int):
    request = task_manager_pb2.DeleteRequest(id=str(id))
    try:
        stub.Delete(request)
        return "Tarefa apagada"
    except grpc.RpcError as e:
        print(e.details(), flush=True)
