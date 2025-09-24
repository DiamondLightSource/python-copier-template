# The developer stage is used as a devcontainer including dev versions
# of the build dependencies
FROM ghcr.io/diamondlightsource/ubuntu-devcontainer:noble AS developer

# Add any system dependencies for the developer/build environment here
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz && \
    apt-get dist-clean
