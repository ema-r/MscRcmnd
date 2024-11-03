
# MscRcmnd - Music Recommender

Music Recommender (or MscRcmnd) is a music recommender service instance that uses containerized microservices to offer the service itself and a bundled web interface, developed for the 23/24 edition of the Laboratory of Advanced Programming course held in Sapienza University of Rome.

## 1. Prerequisites

The system only requires docker and docker-compose installed to run. Make sure that the docker service is active before attempting to run/build.

Clone the repository:
```bash
git clone https://github.com/ema-r/MscRcmnd.git
```

The application requires some Spotify API credentials to be filled in in interfacespot/spotify_secrets.py. The datasets are not provided, and need to be acquired elsewhere
and inserted in the mlengine folder.

## 2. Building and running

To build and run the application:

```bash
docker compose up --build
```
Admin priviledges may be required

---

## 3. Documentation

Documentation is provided under the doc folder.
