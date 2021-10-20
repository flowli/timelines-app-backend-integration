FROM python:3.10-bullseye

RUN pip3 install python-dotenv==0.17.0 imapclient==2.2.0 pickledb==0.9.2 requests==2.25.1

CMD ["python", "/app/run.py"]
