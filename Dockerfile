FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD ./certificador .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]