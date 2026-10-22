FROM --platform=linux/amd64 python:3.11.17-slim-bookworm@sha256:8fb0b110b022c70cbe09d3ff1fb313654f31f9c814abb0d48180af56d906a199

ARG CHROME_VERSION=156.0.8078.47
ARG CHROME_SHA256=e6c94490f0b6b337225aeb2d2a5034858516b7017356980ba94f5176d8774a50
ARG CHROMEDRIVER_SHA256=2a5024610c53f340a1aaa5d9a3e2a4fa448be7d71cca5238bd8c3c7f16181df4

ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8 \
    PYTHONUNBUFFERED=True \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt

RUN apt-get update && apt-get install --no-install-recommends -y \
      ca-certificates=20250419~deb12u2 \
      curl \
      fonts-ipafont-gothic \
      fonts-ipafont-mincho \
      fonts-liberation \
      libasound2 \
      libatk-bridge2.0-0 \
      libatk1.0-0 \
      libatspi2.0-0 \
      libcairo2 \
      libcups2 \
      libdbus-1-3 \
      libdrm2 \
      libgbm1 \
      libglib2.0-0 \
      libgtk-3-0 \
      libnspr4 \
      libnss3 \
      libpango-1.0-0 \
      libu2f-udev \
      libvulkan1 \
      libx11-6 \
      libx11-xcb1 \
      libxcb1 \
      libxcomposite1 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxkbcommon0 \
      libxrandr2 \
      unzip \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    curl --fail --location --retry 3 --output /tmp/chrome.zip \
      "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip"; \
    echo "${CHROME_SHA256}  /tmp/chrome.zip" | sha256sum --check --status; \
    curl --fail --location --retry 3 --output /tmp/chromedriver.zip \
      "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"; \
    echo "${CHROMEDRIVER_SHA256}  /tmp/chromedriver.zip" | sha256sum --check --status; \
    unzip -q /tmp/chrome.zip -d /opt; \
    unzip -q /tmp/chromedriver.zip -d /tmp; \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver; \
    chmod 0755 /usr/local/bin/chromedriver; \
    ln -s /opt/chrome-linux64/chrome /usr/local/bin/google-chrome; \
    rm -rf /tmp/chrome.zip /tmp/chromedriver.zip /tmp/chromedriver-linux64

COPY requirements.lock /tmp/requirements.lock
RUN python -m pip install --no-cache-dir --upgrade pip==26.2.2 && \
    python -m pip install --no-cache-dir --require-hashes -r /tmp/requirements.lock

WORKDIR /tmp/screenshot
COPY screenshot.py /tmp/screenshot.py

ENTRYPOINT ["python", "/tmp/screenshot.py"]
CMD ["--help"]
