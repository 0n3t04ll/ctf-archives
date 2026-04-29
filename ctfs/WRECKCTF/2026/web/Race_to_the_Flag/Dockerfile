FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip 'setuptools<81' wheel \
 && python -m pip install -r requirements.txt
COPY server.py .
COPY .env .
COPY flag.txt /flag.txt
EXPOSE 8080
CMD ["gunicorn", "-w", "4", "--threads", "4", "-t", "30", "--graceful-timeout", "30", "-b", "0.0.0.0:8080", "server:app"]
