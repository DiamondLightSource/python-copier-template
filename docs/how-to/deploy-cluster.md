# How to deploy containers to Kubernetes cluster

If your project is a service with a `Dockerfile`, you may wish to deploy it in a Kubernetes cluster.

## Creating a Helm chart

Helm bundles multiple Kubernetes resources into a single top level resource, `Chart`, and templates resources to inject specified `values`.

```
    service/
    ├── Chart.yaml    # Definition of the resource
    ├── values.yaml   # Defaults for templating
    ├── charts/       # [Optionally] other charts to deploy with
    └── templates/    # Templated Kubernetes resources
```

`templates/` may include at least:
- `deployment.yaml`: creates a pod including your container image
- `service.yaml`: manages Kubernetes networking, potentially exposing your service
- `ingress.yaml`:  optionally maps a DNS entry to the Kubernetes networking

Using `helm create` ensures your service is using the latest standards, therefore Helm resources are not included in this template.
To avoid collisions and to maintain a neat repository, it is recommended to run `helm create <service name>` inside a directory named `helm/` in the root of your repository.

Assuming your container is published to the GitHub container registry, modify your `values.yaml` to deploy your built container.

```yaml
image:
  repository: ghcr.io/<organisation>/<service>
  pullPolicy: Always
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""
```

The container will use the `ENTRYPOINT` and `CMD` defined in your `Dockerfile`.

It is recommended to preserve all of the templates within `templates/`: resources you do not need can be disabled from `values.yaml` while maintaining the ability to deploy or extend the chart.

## Enabling container debugging

The generated `Dockerfile` installs debugpy and with a few modifications can enable remote debugging of a service deployed inside a cluster.

Adding the following to your `values.yaml` gives a standard way of enabling/disabling debugging and documenting the configuration.

```yaml
# Use `kubectl port forward` to access from your machine
debug:
  # Whether the container should start in debug mode
  enabled: false
  # Whether to suspend the process until a debugger connects
  suspend: false
  # Port to listen for the debugger on
  port: 5678
```

The `ENTRYPOINT` and `CMD` concepts in the Dockerfile are analogous to Kubernetes' `command` and `args`.
If `command` is set, it overrides `ENTRYPOINT` and uses `args` if set, ignoring `CMD`.
If `args` is set, `ENTRYPOINT` remains and `CMD` is replaced.

Assuming your `Dockerfile` contains the following, or analogous:

```Dockerfile
ENTRYPOINT ["python"]
CMD ["-m", "service", "--version"]
```

Modifying `deployment.yaml` in the following way allows for your service to enable debugging via the configuration added to `values.yaml`.

```yaml
      containers:
        - ...
          args:
          {{- if .Values.debug.enabled}}
          - "-Xfrozen_modules=off"
          - "-m"
          - "debugpy"
          {{- if .Values.debug.suspend }}
          - "--wait-for-client"
          {{- end }}
          - "--listen"
          - "0.0.0.0:{{ .Values.debug.port }}"
          {{- end }}
          - "-m"
          - "service"
          - "--version"
```

## Connecting to debug mode container

`kubectl port forward` forwards your development machine's port 5678 to the container's:

```sh
$ kubectl get pods
NAME      READY   STATUS    RESTARTS     AGE
service   1/1     Running   0 (1h ago)   1h
$ kubectl port forward pod/service 5678:5678
Forwarding from 127.0.0.1:5678 -> 5678
```

Check out the version of your service that was built into the container and configure your IDE to attach to a remote debugpy process:

The following is a launch configuration from VSCode `launch.json`.
`"remoteRoot"` should match for the version of Python your `Dockerfile` is built from and use your service's name.
`"justMyCode": False` was found to be required for breakpoints to be active.
`"autoReload"` Configured hot swapping of code from your developer machine to the deployed instance.

> ⚠️ **Changes made by autoReload are not preserved.** Code changes made while debugging or resolving an issue should be committed, pushed and built into a new container as soon as possible.


```json
{
  "name": "Python Debugger: Remote Attach",
  "type": "debugpy",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  },
  "pathMappings": [
    {
      "localRoot": "${workspaceFolder}/src",
      "remoteRoot": "/venv/lib/<Python version>/site-packages/<service>"
    }
  ],
  "justMyCode": false,
  "autoReload": {
    "enable": true,
    "exclude": [
      "**/.git/**",
      "**/__pycache__/**",
      "**/node_modules/**",
      "**/.metadata/**",
      "**/site-packages/**"
    ],
    "include": [
      "**/*.py",
      "**/*.pyw"
    ]
  }
}
```

