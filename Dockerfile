FROM python:3.10-alpine

ARG KEY

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENV OPENAI_API_KEY=$KEY
CMD ["python3", "app/app.py"]
