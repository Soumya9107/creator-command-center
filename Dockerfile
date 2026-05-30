FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://withcoral.com/install.sh | sh

RUN pip3 install anthropic google-generativeai groq --break-system-packages

WORKDIR /app

COPY . .

ENV PATH="/root/.local/bin:$PATH"

CMD ["bash"]