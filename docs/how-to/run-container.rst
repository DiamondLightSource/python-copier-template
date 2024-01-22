Run in a container
==================

Pre-built containers with python3-pip-skeleton-cli and its dependencies already
installed are available on `Github Container Registry
<https://ghcr.io/DiamondLightSource/python3-pip-skeleton-cli>`_.

Starting the container
----------------------

To pull the container from github container registry and run::

    $ docker run --rm ghcr.io/DiamondLightSource/python3-pip-skeleton-cli:main --version

To get a released version, use a numbered release instead of ``main``.
