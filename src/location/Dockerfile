FROM public.ecr.aws/docker/library/python:3.10-slim

COPY /src/location-service /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]