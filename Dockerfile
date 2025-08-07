# The developer stage is used as a devcontainer including dev versions
# of the build dependencies
FROM ghcr.io/diamondlightsource/ubuntu-devcontainer:noble AS developer
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    libevent-dev \
    libreadline-dev
