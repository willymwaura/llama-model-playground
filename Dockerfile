# Use an official PyTorch image from the PyTorch project as a parent image
FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install wget
RUN apt-get update && apt-get install -y wget && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the model folder from AWS S3
RUN wget -O llama-2-7b.zip "https://farsightsacco.s3.us-east-2.amazonaws.com/llama-2-7b.zip"

# Install unzip
RUN apt-get update && apt-get install -y unzip && apt-get clean && rm -rf /var/lib/apt/lists/*

# Unzip the downloaded model
RUN unzip llama-2-7b.zip -d llama-2-7b && rm llama-2-7b.zip

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]


