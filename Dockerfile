FROM python:3.8-slim
LABEL huyp="huy.phamquang@cxview.ai"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python3","-u" , "main.py"]
