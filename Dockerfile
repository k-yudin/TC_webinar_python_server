FROM ubuntu

RUN apt update -y
RUN apt install -y python3

RUN mkdir /local/

COPY main.py /local/

EXPOSE 80
CMD ["python3", "/local/main.py"]
