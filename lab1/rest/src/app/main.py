#from fastapi import FastAPI

#app = FastAPI()

#@app.get("/")
#def root():
 #   return {"message": "hello world"}

#@app.get("/count")
#def get_count():
#    global counter
#    counter += 1
#    return counter


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tarefas = list()

class Tarefa(BaseModel):
    tarefa: str
    prioridade: int
    feito: bool

@app.get("/")#caminho é raiz
def root():
    return tarefas

@app.get("/tarefa/{pos}")
def get_tarefa(pos: int):
    return tarefas[pos]

@app.post("/adicionar/")
def criar_tarefa(tarefa: Tarefa):
    tarefa.feito = False
    tarefas.append(tarefa)
    return len(tarefas)

@app.put("/feito/{pos}")
def marcar_feito(pos: int):
    tarefas[pos].feito = True
    return tarefas[pos]

@app.delete("/deletar/{pos}")
def deletar_tarefa(pos: int):
    tarefa = tarefas.pop(pos)
    return tarefa

#código principal da api rest

#contem:
#-api fastapi com endpoints para gerenciar tarefas
#operacoes: get, post, put, delete
#modelo pydativ: tarefa com validacao

#endpoints:
#get: lista todas as tarefas
#get/tarefa/{pos}: pega tarefa especifica
#post/adicionar/: adiciona nova tarefa
#put /feito/{pos}: marca tarefa como feita
#delete /deletar/{pos}: remove tarefa