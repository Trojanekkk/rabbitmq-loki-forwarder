# rabbitmq-loki-forwarder
A simple Python script / app for pushing internal RabbitMQ messages fromS queue to the Loki instance.

For more details look for _Event Exchange Plugin_.

## Usage

Run the app in the docker container with the default setup:

```
docker run -d ghcr.io/trojanekkk/rabbitmq-loki-forwarder:1.0.0
```

For almost 100% you will want to configure the app to make it work within your environment. To modify the default behaviour use environment variables. The following are allowed:

- `FORWARDER_LOKI_HOST` (defaults to _localhost_) - Hostname or IP address of the Loki server
- `FORWARDER_LOKI_PORT` (defaults to _3100_) - Port of the Loki server
- `FORWARDER_RABBIT_HOST` (defaults to _localhost_) - Hostname or IP address of the RabbitMQ server
- `FORWARDER_RABBIT_PORT` (defaults to _5672_) - Port of the RabbitMQ server
- `FORWARDER_RABBIT_USERNAME` (defaults to _admin_) - Username to authorize with the RabbitMQ server
- `FORWARDER_RABBIT_PASSWORD` (defaults to _admin_) - Password to authorize with the RabbitMQ server
- `FORWARDER_RABBIT_QUEUE` (defaults to _event_queue_) - Name of the Queue in the RabbitMQ server which is bound to the Event Exchange (check Event Exchange Plugin for more details) 
- `FORWARDER_APPLICATION_NAME` (defaults to _rabbitmq-loki-forwarder_) - Tag added to every message in the queue for filtering data in e.g. Grafana

For example:

```
docker run -d -e FORWARDER_LOKI_HOST=192.168.1.1 -e FORWARDER_LOKI_PORT=4321 ghcr.io/trojanekkk/rabbitmq-loki-forwarder:1.0.0
```
