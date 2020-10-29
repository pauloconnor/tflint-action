FROM alpine:3.12

LABEL version="0.0.1"
LABEL name="tflint-action"
LABEL repository="http://github.com/paulocnnor/tflint-action"
LABEL homepage="http://github.com/pauloconnor/tflint-action"
LABEL maintainer="Paul O'Connor<paul@poconnor.me>"

LABEL "com.github.actions.color"="red"
LABEL "com.github.actions.description"="Run tflint against your Terraform repositories"
LABEL "com.github.actions.icon"="terminal"
LABEL "com.github.actions.name"="tflint"

RUN apk add --update --no-cache bash ca-certificates curl git jq python3 py3-pip
RUN pip3 install gitpython
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -Ls https://github.com/terraform-linters/tflint/releases/latest/download/tflint_linux_amd64.zip \
    -o /tmp/tflint.zip && \
    unzip /tmp/tflint.zip -d /usr/local/bin && \
    rm /tmp/tflint.zip

COPY main.py /main.py
CMD ["/main.py"]
