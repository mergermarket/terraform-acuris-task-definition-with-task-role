FROM python:3-alpine
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.12.18
ENV TERRAFORM_ZIP=terraform_${TERRAFORM_VERSION}_linux_amd64.zip
ENV TERRAFORM_SUM=e7ebe3ca988768bffe0c239d107645bd53515354cff6cbe5651718195a151700

ENV PYTHONDONTWRITEBYTECODE donot

RUN apk add -U ca-certificates curl git && \
    cd /tmp && \
    curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${TERRAFORM_ZIP} && \
    echo "${TERRAFORM_SUM}  /tmp/${TERRAFORM_ZIP}" | sha256sum -c - && \
    unzip /tmp/${TERRAFORM_ZIP} -d /usr/bin && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
