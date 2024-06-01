FROM pytorch/pytorch:latest

ENV TORCHSERVE_HOME /home/model-server
ENV PATH=$TORCHSERVE_HOME/bin:$PATH

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install torchserve torch-model-archiver

RUN pip install --no-cache-dir torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-2.3.0+cu121.html

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/local/bin/
COPY . .

RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chmod +r model_weights.pth

EXPOSE 8080 8081

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
