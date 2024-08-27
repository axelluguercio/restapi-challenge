# REST API Challenge

## Overview

This project implements a REST API based on the provided OpenAPI/Swagger definition using Python. The API includes endpoints for health checks, Prometheus metrics, DNS resolution, IP validation, and query history retrieval. The service is Dockerized and can be deployed to Kubernetes with custom helm chart for backend services.

## Features

- **/metrics**: Exposes Prometheus metrics for monitoring.
- **/health**: Provides a health check endpoint.
- **/** (root): Returns the current date (UNIX epoch), version, and whether the application is running under Kubernetes.
- **/v1/tools/lookup**: Resolves IPv4 addresses for a given domain and logs the queries in a database.
- **/v1/tools/validate**: Validates if the input is an IPv4 address.
- **/v1/history**: Retrieves the latest 20 saved queries from the database.

## Example Output for Root Endpoint

```json
{
  "version": "0.1.0",
  "date": 1663534325,
  "kubernetes": false
}

## CI Pipeline

The CI pipeline run a python linter using flake8, build the docker image and push it to public docker registry.

## Kubernetes

Custom helm chart for backend service, using external secrets for secrets, multiple cloud provider supported (Azure, Aws, GCP)