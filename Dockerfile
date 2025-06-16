# Uses NVIDIA's PyTorch container as base
FROM nvcr.io/nvidia/pytorch:25.03-py3

# Set basic environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install some common packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl wget git libgl1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /workspace

# Install pip packages
RUN pip install timm zod

# Copy
COPY . .

RUN mkdir -p /data_zod
RUN tar -xzvf /workspace/data/drives_mini.tar.gz -C ../data_zod
RUN tar -xzvf /workspace/data/frames_mini.tar.gz -C ../data_zod
RUN tar -xzvf /workspace/data/sequences_mini.tar.gz -C ../data_zod

# Default command - print info and run CUDA test
CMD ["python", "cuda_test.py"]
