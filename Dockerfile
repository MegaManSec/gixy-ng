FROM python:alpine

ADD . /src

WORKDIR /src

RUN pip install --upgrade pip setuptools wheel
# Use pip to install the project so install_requires are honored (e.g., six)
RUN pip install .

ENTRYPOINT ["gixy"]
