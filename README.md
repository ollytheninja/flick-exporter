# Flick Exporter

Exposes Flick Electric power prices as Prometheus metrics so you can put it in a graph 🤷‍.

Utilises [my fork](https://github.com/ollytheninja/PyFlick) of [Drian Naude's work](https://github.com/driannaude/PyFlick).

## Deploying

### Kubernetes

If you have a Kubernetes Cluster running the prometheus operator, 
you can use `manifest.yaml` to deploy this script and a ServiceMonitor.

First update and deploy `secrets.yaml` with your Flick username and password (in base 64).
Then deploy `manifest.yaml`.

### Docker

The app requires setting your Flick Electric username and password as environment variables.
Everything else is taken care of.

    docker run -p 8000:8000 \ 
    -e "FLICK_USERNAME=tommy@tester.com" \
    -e "FLICK_PASSWORD=supersafepassword" \
    ghcr.io/ollytheninja/flick-exporter:latest
