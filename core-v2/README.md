# Upstage Setup Guide

This guide will help you set up and run the Upstage application using Docker.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### 1. Configure Environment Variables

Go to the `config_formatted_date.py` file and update your environment variables as needed.

### 2. Start the Application

You can start the Upstage application using either a single container or multiple containers.

#### Single Container

To start the application using a single container, run the following command:

```sh
cd single-container
sh startup.sh
```

#### Multiple Containers

To start the application using multiple containers, use Docker Compose. First, ensure you have a `docker-compose.yml` file configured. Then, run the following command:

```sh
cd mutilple-containers
docker-compose up -d
```

This will start all the services defined in your `docker-compose.yml` file.