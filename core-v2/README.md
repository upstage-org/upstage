# Upstage Setup Guide

This guide will help you set up and run the Upstage application using Docker.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### 1. Configure Environment Variables

Go to the `config_formatted_date.py` file and update your environment variables as needed.

### 2. Run Docker Containers

To start the Docker containers, run the following command:

```sh
docker-compose up -d
```

This command will build and start the containers in detached mode.

### 3. Run Scripts
To run scripts within the Upstage backend container, follow these steps:

1. Access the Upstage backend container:

```sh
docker exec -it upstage /bin/bash
```

2. Export the TIMESTAMP environment variable:

```sh
export TIMESTAMP=$(date +"%d_%m_%Y")
```