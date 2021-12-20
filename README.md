## Decision-Making

### Problem  
A customer that 
* primarily uses Go or Python for its services and runs them in a containerized environment (linux)
* has tools to monitor log files and
* is actively looking for developers with knowledge of Prometheus

requires a simple but easily extensible solution to monitor health of a webservice.  

### Implementation Proposal
* Use Prometheus to store the information about the service's health. 
* Write a simple exporter that retrieves the service's HTTP status code.
* Add a Grafana dashboard to display the collected data
* Create an alert to verify that Prometheus receives the data from exporter
* Create an alert to notify the customer about the webservice failures. Note: since the customer's webservice is quite flaky it might make sense to only notify customer about long term disruptions.
* Use [the multiple target pattern](https://prometheus.io/docs/guides/multi-target-exporter/) for the exporter so that if the customer would want to monitor any further services it could be done just be adding a new endpoint url to a config.

### Other Options Considered
* Telegraf + InfluxDB/Prometheus 
  * pros: low effort
  * cons: doesn't match the customer's stack
* Prometheus + BlackBox Exporter
  * pros: low effort
  * cons: customer wants a solution that is not "too abstract". Usage of Blackbox Exporter doesn't match this requirement.

## About The Project

Prometheus-based website health monitor. This project is a multi-container application that runs
* the prometheus engine itself
* a simple Python-based custom exporter for the prometheus
* Grafana with pre-configured dashboard to visualize the collected data

## Getting Started
Clone the repo
```sh
git clone https://github.com/zxspectrummy/webservice-monitor.git
```
Then, make sure you have docker and [docker-compose](https://docs.docker.com/compose/) installed and run

    $ docker-compose build

    >>> start all the containers. Run without the `-d` if you want to see container logs.
    $ docker-compose up -d

A simple diagram showing the http status code returned by the webservice will now be available at
http://localhost:3000/dashboards

To check the monitoring system health go to http://localhost:9090/alerts

## Usage

### Configure webservices to monitor
To add/remove webservices that should be monitored just adjust `config/targets.yml` (no Prometheus restart required)

## Roadmap

- [x] MVP to demo the basic features:
  - check webservice http status code
  - save the results in Prometheus
  - Grafana dashboard to visualize the data
- [x] Support monitoring multiple webservices
- [ ] Add alertmanager to handle the alerts
  - since customer has a logs monitoring system in future it might make sense to save the alerts in the log file
- [ ] Deploy the app in K8


## Testing

### Prometheus Configuration Testing
Tests for the alerting rules are available in `/config/test_rules.yml` 
To run the tests execute
``` 
docker run -v $(pwd)/config:/config -it --entrypoint=promtool prom/prometheus:v2.32.0 test rules /config/test_rules.yml
```
Note: on Windows to avoid issues with mounting the config volume use
```
$ MSYS_NO_PATHCONV=1 docker run -v $(pwd)/config:/config -it --entrypoint=promtool prom/prometheus:v2.32.0 test rules /config/test_rules.yml
```