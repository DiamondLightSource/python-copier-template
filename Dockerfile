# The devcontainer should use the developer target and run as root with podman
# or docker with user namespaces.
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} AS developer

# Use this version of uv
ARG UV_VERSION=0.7

# Install uv using the official image
# See https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:${UV_VERSION} /uv /uvx /bin/
