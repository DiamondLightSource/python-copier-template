# Debug a container within a cluster

The container build also publishes a debug container for each tagged release of the container with the tag suffixed with `-debug`. This container contains the workspace and has an alternative entrypoint which allows the devcontainer to attach: so if you have configured a `livenessProbe` that requires the service to have started it should be disabled. The container also installs debugpy and makes the service install editable. Any custom `command` or `args` defined for the container should be disabled.

With the [Kubernetes plugin for vscode](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools) it is then possible to attach to the container inside the cluster. This may require that the kubeconfig is at `~/.kube/config`, rather than referenced from the environment variable `KUBECONFIG`. It may also be necessary to [add additional contextual information](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_config/kubectl_config_set-context/), such as the namespace in use.

![Location of the Kubernetes plugin in the plugin bar (screen left), with the Clusters>cluster>Workloads>Pods views expanded out to show a pod named "my-service", overlaid with a dropdown box, with the "Attach Visual Studio Code" highlighted](../images/debugging-kubernetes.jpg)
The Kubernetes plugin can be found in the plugin bar. Expanding the Clusters>`cluster`>Workloads>Pods views, your service should be visible. Right Click>Attach Visual Studio Code will initiate connecting to the workspace in the cluster. Select your service container from the top menu.

After the connection to the cluster has been established, it may be necessary to open the workspace folder by clicking the Explorer option in the plugin bar, it should be mounted at `/workspaces/<service name>`, equivalent to a local devcontainer.

Starting your service with the command usually executed by the container definition starts it on the node, with access to kubernetes resources as usual, however it's also now possible to attach a debugger, configured to autoReload code, or to start and stop the service rapidly to implement prospective changes.

After you are happy with the changes, commit them and release a new version of your container. Changes will otherwise not be persisted across container restarts! Your git configuration should be mounted inside the container.

## Debugging containers that run as non-root
For containers running in the Diamond Kubernetes infrastructure that run as a specific uid (e.g. if mounting the filesystem), it is required to use a sidecar container to provide name resolution with Diamond's LDAP infrastructure and to mount a home directory to download vscode plugins. 

A sidecar for the Debian-based Python image this template uses is published as a container from this repository, the version should match the version of the python-copier-template you are using, to ensure compatibility with the underlying container infrastructure.

```yaml
- name: debug-account-sync
    image: ghcr.io/diamondlightsource/python-copier-template/account-sync:<version>
    volumeMounts:
    # This allows the nslcd socket to be shared between the main container and the sidecar
    - mountPath: /var/run/nslcd
    name: nslcd
```

The following changes/additions to your `values.yaml` will be required to connect vscode when using the sidecar.

```yaml
volumes:
- name: home  # Required for vscode to install plugins
  hostPath:
    path: /home/
- name: nslcd  # Shared volume between main and sidecar container
  emptyDir:
    sizeLimit: 500Mi

volumeMounts:
- mountPath: /home/
  name: home
- mountPath: /var/run/nslcd
  name: nslcd

# Disable any liveness probe, as will not start service automatically
livenessProbe:

# Required to mount /home/, /dls/ etc.
podSecurityContext:
  runAsUser: <uid>
  runAsGroup: <gid>

image:
  tag: "<version>-debug"
```
