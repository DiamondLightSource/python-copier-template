# Debugging containers

The container build also publishes a debug container for each tagged release of the container suffixed with `-debug`. This container contains an editable install of the workspace & debugpy and has an alternate entrypoint which allows the devcontainer to attach.

# Using Debug image in a Helm chart

⚠️ If running with the Diamond filesystem mounted or as a specific user, further adjustments are required, as described in the next section.

To use the debug image in a Helm chart can be as simple as modifying `image.tag` value in values.yaml to the tag with `-debug`, but this may run into issues if you have defined liveness or readiness probes, a custom command or args, or if the container is running as non-root. To make capturing these edge cases easier it's recommended to define a single flag `debug.enabled` in your `values.yaml` and make the following modifications to the `Deployment|ReplicaSet|StatefulSet`:

```yaml
spec:
  template:
    spec:
      containers:
        - image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}{{ ternary "-debug" "" .Values.debug.enabled }}"
          {{- if not .Values.debug.enabled }}  # If your Helm chart overrides the `CMD` Containerfile instruction, it should not when in debug mode
          args: ["some", "example", "args"]
          {{- end }}
          {{- if not .Values.debug.enabled }}  # prevent probes causing issues before attaching and starting the service
          {{- with .Values.livenessProbe }}
          livenessProbe:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.readinessProbe }}
          readinessProbe:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- end }}
          volumeMounts:
          {{- if .Values.debug.enabled }}
          - mountPath: /home  # required for VSCode to install extensions if running as non-root
            name: home
          {{- end }}
          {{- with .Values.volumeMounts }}
            {{- toYaml . | nindent 12 }}
          {{- end }}
      volumes:
        {{- if .Values.debug.enabled }}
        - name: home  # mount /home as an editable volume to prevent permission issues
          emptyDir:
            sizeLimit: 500Mi
        {{- end }}
        {{- with .Values.volumes }}
          {{- toYaml . | nindent 8 }}
        {{- end }}
```

# Using Debug image in a Helm chart that mounts the filesystem

Containers running in the Diamond Kubernetes infrastructure as a specific uid (e.g. when mounting the filesystem) must provide name resolution from Diamond's LDAP infrastructure: inside the cluster the VSCode server will be running as that user, but requires that the name & home directory of the user can be found. The debug image configures the name lookup service to try finding the user internally (i.e. from `/etc/passwd`) then fall back to calling LDAP through a service called `libnss-ldapd`. As containers are designed to run a single process, this service is run in a sidecar container which must mutually mount the `/var/run/nslcd` socket with the primary container.

It therefore requires the further additions to the template modified above:

```yaml
spec:
  template:
    spec:
      containers:
        - volumeMounts:
          {{- if .Values.debug.enabled }}
          - mountPath: /var/run/nslcd  # socket to place query for user information
            name: nslcd
          [...]
        {{- if .Values.debug.enabled }}
        - name: debug-account-sync
          image: ghcr.io/diamondlightsource/account-sync-sidecar:3.0.0
          volumeMounts:
          - mountPath: /var/run/nslcd  # socket to pick queries for user information
            name: nslcd
        {{- end }}
      volumes:
        {{- if .Values.debug.enabled }}
        - name: nslcd  # mutually mounted filesystem to both containers
          emptyDir:
            sizeLimit: 5Mi
          [...]
```

# Debugging in the cluster

With the [Kubernetes plugin for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools) it is then possible to attach to the container inside the cluster. From the VSCode Command Palette (Ctrl+Shift+P) use the `Kubernetes: Set Kubeconfig` to configure VSCode with the server to use, then`Kubernetes: Use Namespace`.

```sh
# To find the KUBECONFIG to use from a Diamond machine
$ module load pollux
...
$ echo $KUBECONFIG
~/.kube/config_pollux
```

![Location of the Kubernetes plugin in the plugin bar (screen left), with the Clusters>cluster>Workloads>Pods views expanded out to show a pod named "my-service", overlaid with a dropdown box, with "Attach Visual Studio Code" highlighted](../images/debugging-kubernetes.jpg)
The Kubernetes plugin can be found in the plugin bar. Expanding the Clusters>`cluster`>Workloads>Pods views, your service should be visible. Right Click>Attach Visual Studio Code will initiate connecting to the workspace in the cluster. Select your service container from the top menu when prompted.

After the connection to the cluster has been established open the workspace folder by clicking the Explorer option in the plugin bar, the repository will be mounted at `/workspaces/<service name>`, equivalent to when working with a local devcontainer.

Starting your service with the command in the container definition starts it on the node, with access to Kubernetes resources, however it is also now possible to run with or attach a debugger, potentially configured to autoReload code, or to start and stop the service rapidly to implement prospective changes.

After you are happy with the changes, commit them and release a new version of your container. Changes will otherwise not be persisted across container restarts. Your git and ssh config will be mounted inside the devcontainer while connected and for containers on github, the remote `origin` will be configured to use ssh.
