FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV TZ=Asia/Shanghai

LABEL maintainer="chensl <l1328076914@gmail.com>"

COPY requirements.txt .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app/

ENV PYTHONPATH=/app
