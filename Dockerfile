# Use Debian bookworm slim image
FROM debian:bookworm-slim

# Set environment variables to non-interactive (to avoid prompts during installation)
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y && apt install -y python3 python3-venv python3-pip && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/script/venv && python3 -m venv /opt/script/venv

RUN /opt/script/venv/bin/pip install --no-cache-dir --upgrade pip && /opt/script/venv/bin/pip install --no-cache-dir requests bs4 lxml

COPY getData.py /opt/script/getData.py

RUN chmod +x /opt/script/getData.py
RUN mkdir -p /opt/script/output

ENTRYPOINT /opt/script/venv/bin/python3 /opt/script/getData.py --password $PASSWORD \
                       --username $USERNAME \
                       --url $URL \
                       --output_file $OUTPUT_FILE
