FROM public.ecr.aws/docker/library/ubuntu:22.04

## CPU DOCKERFILE

ARG BLENDER_VERSION=${BLENDER_VERSION}
ARG BLENDER_VERSION_MAJOR=${BLENDER_VERSION_MAJOR}
ENV BLENDER_URL https://mirror.clarkson.edu/blender/release/Blender${BLENDER_VERSION}/blender-${BLENDER_VERSION_MAJOR}-linux-x64.tar.xz

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y \
    sudo \
    curl \
    ca-certificates \
    zip \
    xz-utils \
    python3 \
    python3-pip \
    xvfb \
    tree

# Download and install Blender
RUN curl "${BLENDER_URL}" -o "blender.tar.xz" && \
    tar -xvf blender.tar.xz --strip-components=1 -C /bin && \
    rm -rf blender.tar.xz && \
    rm -rf blender

RUN apt-get update -y && \
    apt-get install -y \
    libx11-dev \
    libxi-dev \
    libxxf86vm-dev \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libsm6 \
    libwayland-client0 \
    libwayland-server0

RUN pip3 install boto3
RUN pip install requests


# EFS ENV
ENV EFS_BLENDER_FOLDER_PATH=/mnt/efs/projects
ENV EFS_BLENDER_OUTPUT_FOLDER_PATH=/mnt/efs/projects/project-2/output
ENV EFS_BLENDER_FILE_PATH=/mnt/efs/projects/project-2/3.3.0-scene.blend

# Blender ENV
ENV BLENDER_EXECUTABLE=/usr/bin/blender

# Job Action type
ENV JOB_ACTION_TYPE=render


# Copy specific folders and their contents
COPY ./app /app

# Give execute permissions to the script
RUN chmod +x /app

WORKDIR /

ENTRYPOINT ["python3", "/app/app.py"]
 