# Deploy with Helm

If your project is a service, you may wish to deploy it into a Kubernetes cluster using Helm. 
If enabled, a `helm/` directory is created, which bundles Kubernetes resources into a top level resource, `Chart`, and templates resources to inject specified `values`.

```
    service/
    ├── Chart.yaml    # Definition of the resource
    ├── values.yaml   # Defaults for templating
    ├── charts/       # [Optionally] other charts to deploy with
    └── templates/    # Templated Kubernetes resources
```

`templates/` includes among others:
- `deployment.yaml`: creates a pod including your container image
- `service.yaml`: manages Kubernetes networking, potentially exposing your service
- `ingress.yaml`:  optionally maps a DNS entry to the Kubernetes networking

Assuming your container is published to the GitHub container registry, `values.yaml` will be pre-configured to use your built container and enable debugging.

```yaml
image:
  repository: ghcr.io/{{ organisation }}/{{ repo_name }}
  pullPolicy: Always
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""

# Use `kubectl port forward` to access from your machine
debug:
  # Whether the container should start in debug mode
  enabled: false
  # Whether to suspend the process until a debugger connects
  suspend: false
  # Port to listen for the debugger on
  port: 5678
```

To enable debugging, the CMD arguments of the Dockerfile have been overwritten by the analogous `args` from Kubernetes.
The `ENTRYPOINT` and `CMD` concepts in the Dockerfile are analogous to Kubernetes' `command` and `args`.
If `command` is set, it overrides `ENTRYPOINT` and uses `args` if set, ignoring `CMD`.
If `args` is set, `ENTRYPOINT` remains and `CMD` is replaced.


```yaml
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

It is recommended to preserve all of the templates within `templates/`: resources you do not need can be disabled from `values.yaml` while maintaining the ability to deploy or extend the chart.

## Connecting to a container in debug mode

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
