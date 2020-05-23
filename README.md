# tahskr-server

* [What is tahskr?](#what-is-tahskr)
* [Screenshot](#screenshot)
* [Installation](#installation)
  * [Docker](#docker)
  * [Other](#other)

## What is tahskr?
tahskr is a simple, open source, self-hosted todo manager.

There are two parts to tahskr. The **server side** that stores and serves data (that's this repo) and the [**frontend**](https://github.com/Dullage/tahskr) that provides a web interface accessible from a mobile/desktop browser or Windows Electron app.

Both parts can be self-hosted but you only really need to self-host the server side as [tahskr.com](https://tahskr.com) or the published Electron app can be used to access data on any tahskr server.

## Screenshot

![Screenshot](https://github.com/Dullage/tahskr/blob/master/docs/screenshot.png?raw=true)

## Installation

*Note: These installation instructions relate to the server part of tahskr (this repo). For details about the frontend see [this repo](https://github.com/Dullage/tahskr).*

### Docker

Docker images of all [releases](https://github.com/Dullage/tahskr-server/releases) are published to [Docker Hub](https://hub.docker.com/r/dullage/tahskr-server). These images are built for x86/64 and arm64.

Example Command:

```bash
docker run \
  -d \
  --name tahskr-server \
  -v "/path/for/database:/app/data" \
  -p 80:80 \
  --restart=always \
  dullage/tahskr-server:latest
```

### Other

This is a flask python app so can be deployed in a number of different ways. See the [Flask Docs](https://flask.palletsprojects.com/en/1.1.x/deploying/) for details.

## API Reference

See the API docs [here](https://github.com/Dullage/tahskr-server/blob/master/docs/api.md).
