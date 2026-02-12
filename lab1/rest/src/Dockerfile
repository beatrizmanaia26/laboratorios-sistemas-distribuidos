#receita para construir uma imagem docker

FROM python:3.13.7-alpine3.21 
#imagem base leve

WORKDIR /app
#diretorio de trabalho

COPY ./requirements.txt /code/requirements.txt
#copia dependencias

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#instala bibliotecas

COPY ./app/* .
#copia codigo da aplicacao

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
#comando para iniciar

#funcao do arq: ensinar docker como empactoar a aplicacao