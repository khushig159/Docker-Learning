FROM python

WORKDIR /python

#COPY ./myapp.py .
# COPY ./server.txt .
#COPY ./api_demo.py . 
COPY ./sqldemo.py . 


RUN pip install pymysql
RUN pip install cryptography

CMD ["python", "sqldemo.py"]

