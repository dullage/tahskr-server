# tahskr-server

* [What is tahskr?](#what-is-tahskr)
* [Screenshot](#screenshot)
* [Installation](#installation)
  * [Docker](#docker)
  * [Other](#other)

## What is tahskr?
tahskr is a simple, open source, self-hosted todo manager.

There are two parts to tahskr. The **server side** that stores and serves data (that's this repo) and the [**frontend**](https://github.com/Dullage/tahskr) that provides a web interface accessible from a mobile/desktop browser or Windows Electron app.

## Screenshot

![Screenshot](https://github.com/Dullage/tahskr/blob/master/docs/screenshot.png?raw=true)

## Installation

*Note: These installation instructions relate to the server part of tahskr (this repo). For details about the frontend see [this repo](https://github.com/Dullage/tahskr).*

### Docker

Docker images of all [releases](https://github.com/Dullage/tahskr-server/releases) are published to [Docker Hub](https://hub.docker.com/r/dullage/tahskr-server). These images are built for x86/64 and arm64.

Example Docker Run Command:

```bash
docker run -d \
  --name tahskr-server \
  -e "TAHSKR_ADMIN_PASSWORD=changeMe!" \
  -v "/path/for/database:/app/data" \
  -p 8080:8080 \
  --restart=unless-stopped \
  dullage/tahskr-server:latest
```

Example Docker Compose:

```bash
version: "3"

services:
  tahskr:
    container_name: tahskr-server
    image: dullage/tahskr-server:latest
    environment:
      TAHSKR_ADMIN_PASSWORD: "changeMe!"
    volumes:
      - "/path/for/database:/app/data"
    ports:
      - "8080:8080"
    restart: unless-stopped
```

Once running, you can use the API to create a user account. See the [API docs](https://github.com/Dullage/tahskr-server/blob/master/docs/api.md) for details.

Example Curl Command:

```bash
curl -X POST http://[SERVER IP OR NAME]:[YOUR PORT]/user -H 'Content-Type: application/json' -H 'x-admin: [YOUR ADMIN PASSWORD]' -d '{ "username": "[YOUR USERNAME]", "password": "[YOUR PASSWORD]"}'
```

### Other

This is a flask python app so can be deployed in a number of different ways. See the [Flask Docs](https://flask.palletsprojects.com/en/1.1.x/deploying/) for details.

## API Reference

See the API docs [here](https://github.com/Dullage/tahskr-server/blob/master/docs/api.md).
