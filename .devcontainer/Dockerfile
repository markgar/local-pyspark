# Pull Spark from the official Docker image (much faster than archive.apache.org)
FROM apache/spark:3.5.0 AS spark

FROM mcr.microsoft.com/devcontainers/base:ubuntu

# -------------------------------------------------------------------
# Match Microsoft Fabric Runtime 1.3
#   Spark 3.5.0 | Java 11 | Scala 2.12.18 | Python 3.11 | R 4.3 | Delta Lake 3.2.0
# -------------------------------------------------------------------

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"
ENV PYSPARK_PYTHON=python3

# Install Python 3.11 and Spark dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    curl \
    software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.11 \
        python3.11-venv \
        python3.11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default and install pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Copy Spark from the official image
COPY --from=spark /opt/spark "${SPARK_HOME}"

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Python packages (baked into image)
RUN pip install --no-cache-dir \
    pyspark==3.5.0 \
    delta-spark==3.2.0 \
    jupyter \
    pandas==2.1.4 \
    numpy==1.26.4 \
    pyarrow==14.0.2 \
    ms-fabric-cli
