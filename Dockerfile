ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} as developer
RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH