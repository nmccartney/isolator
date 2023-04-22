FROM python:3.9-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install base utilities
# RUN add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe"
RUN apt-get update --fix-missing && \
    # apt-get install -y build-essentials  && \
    apt-get install -y wget && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH


# RUN apt-get update --fix-missing && apt-get install -y wget

# RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh

# RUN chmod -v +x Anaconda3-2022.05-Linux-x86_64.sh

# RUN bash Anaconda3-2022.05-Linux-x86_64.sh -b -f

# RUN eval"$(/home/mastodon/anaconda3/bin/conda shell hook)"

# RUN conda config --add channels conda-forge

# RUN conda install -c conda-forge ffmpeg libsndfile

# ------
# RUN apt-get update --fix-missing \
#     && apt-get install -y wget bzip2 ca-certificates curl git \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* \
#     && wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh -O ~/miniconda.sh \
#     && /bin/bash ~/miniconda.sh -b -p /opt/conda \
#     && rm ~/miniconda.sh \
#     && /opt/conda/bin/conda clean -tipsy \
#     && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
#     && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
#     && echo "conda activate base" >> ~/.bashrc \
#     && ln -s /opt/conda/bin/conda /usr/bin/conda
# -----

# ENV CUDA_VERSION 10.0.130
# ENV CUDA_PKG_VERSION 10-0=$CUDA_VERSION-1
# ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
# ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# ENV NVIDIA_VISIBLE_DEVICES=all
# ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
# ENV NVIDIA_REQUIRE_CUDA "cuda>=10.0 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=410,driver<411"
# ENV NCCL_VERSION 2.4.2
# ENV CUDNN_VERSION 7.6.0.64

# LABEL com.nvidia.cuda.version="${CUDA_VERSION}"
# LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"
# LABEL com.nvidia.volumes.needed="nvidia_driver"

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     gnupg2 \
#     curl \
#     ca-certificates \
#     && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - \
#     && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list \
#     && echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list \
#     && apt-get purge --autoremove -y curl \
#     && apt-get update \
#     && apt-get install -y --no-install-recommends \
#     cuda-cudart-$CUDA_PKG_VERSION \
#     cuda-compat-10-0 \
#     && ln -s cuda-10.0 /usr/local/cuda \
#     && echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \
#     && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf \
#     && apt-get install -y --no-install-recommends \
#     cuda-toolkit-10-0 \
#     cuda-libraries-$CUDA_PKG_VERSION \
#     cuda-nvtx-$CUDA_PKG_VERSION \
#     libnccl2=$NCCL_VERSION-1+cuda10.0 \
#     libcudnn7=$CUDNN_VERSION-1+cuda10.0 \
#     && apt-mark hold libnccl2 \
#     && apt-mark hold libcudnn7 \
#     && rm -rf /var/lib/apt/lists/*

# ------

# RUN conda config --add channels conda-forge
# RUN conda install -y -c conda-forge 
# RUN  conda  install  -y -c musdb
# RUN conda install -y -c deezer-research  
# RUN conda install -y -c spleeter 

#  ----

WORKDIR /flask-api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install libgl1 libglib2.0-0 -y
RUN apt-get install -y ffmpeg 
RUN apt-get install -y libsndfile1
RUN apt-get install -y curl
# RUN apt-get --yes install libsndfile1

COPY requirements.txt .


# install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --root-user-action=ignore --no-cache-dir -r requirements.txt

RUN pip3 install celery

RUN pip3 install musdb museval
RUN pip3 install spleeter
# COPY ./gunicorn-cfg.py .
COPY . .

# Cache is invalidated when ARG is USED so put this low in stage
ARG BUILD_DATE
ENV BUILD_DATE="$BUILD_DATE"
ARG GIT_HASH
ENV GIT_HASH="$GIT_HASH"
ARG GIT_TAG=""
ENV GIT_TAG="$GIT_TAG"
ARG BUILD_TYPE=
ENV BUILD_TYPE="$BUILD_TYPE"

# Set the environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

EXPOSE 5000


# FROM builder as dev
# # gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]



FROM builder as watch-dev

COPY --from=builder /flask-api /flask-api

WORKDIR /flask-api

# ENTRYPOINT python ./run.py
