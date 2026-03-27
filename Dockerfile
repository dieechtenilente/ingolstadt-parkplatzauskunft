# Use Debian bookworm slim image
FROM debian:bookworm-slim

# Set environment variables to non-interactive (to avoid prompts during installation)
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y --no-install-recommends python3 python3-pip
RUN rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/* /usr/share/locale/*

RUN pip3 install --no-compile --no-cache-dir requests bs4 lxml

COPY getData.py /opt/script/getData.py

RUN chmod +x /opt/script/getData.py
RUN mkdir -p /opt/script/output

ENTRYPOINT python3 /opt/script/getData.py --password $PASSWORD \
                       --username $USERNAME \
                       --url $URL \
                       --output_file $OUTPUT_FILE
