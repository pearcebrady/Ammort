FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY Loan.py ./
COPY Testfile.py ./

CMD ["python3", "./Testfile.py"]