# Use this version of Python
ARG PYTHON_VERSION=3.11
# Use this version of uv
ARG UV_VERSION=0.7

# Install uv using the official image
# See https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-distroless

# The devcontainer should use the developer target and run as root with podman
# or docker with user namespaces.
FROM python:${PYTHON_VERSION} AS developer

# Add any system dependencies for the developer/build environment here
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     graphviz

# Install from uv image
COPY --from=uv-distroless /uv /uvx /bin/
