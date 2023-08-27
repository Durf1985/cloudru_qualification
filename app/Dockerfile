FROM python:alpine3.18 AS build

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt && \
    pip uninstall -y pip

COPY ./ /app

FROM alpine:3.18

ENV AUTHOR=Aleksey UUID=
RUN adduser --home /app -S cloudru

WORKDIR /app

COPY --from=build /usr/local /usr/local
COPY --from=build /app /app

USER cloudru

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

LABEL maintainer="Loktionov Aleksey" \
    env="cloudru"
