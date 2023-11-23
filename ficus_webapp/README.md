# Ficus OS Webapp
Server side component - currently used for syncing time and environment readings.

## Dependencies

### Python

Install a recent version of Python - this has been tested to work with 3.10 or higher.

### Flask Application Server 

Requires python - always use a recent version.

> pip install Flask

### Start server

Use the following command in the same directory as ```ficus_server.py```

```
flask --app ficus_server run --host=0.0.0.0
```
Control^C to end. This should not be ran in production or on public networks - put it behind a proxy server. See Flask documentation for more details.