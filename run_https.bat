@echo off
if not exist certs\localhost-cert.pem python scripts\generate_cert.py
uvicorn main:app --host 127.0.0.1 --port 8000 --ssl-keyfile certs\localhost-key.pem --ssl-certfile certs\localhost-cert.pem
