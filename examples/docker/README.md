# Running pysrim in docker container

This is an example of running pysrim within the [provided docker
container](https://hub.docker.com/r/costrouc/pysrim/tags/) `costrouc/pysrim`

``` bash
cd examples/docker
docker run -v $PWD:/opt/pysrim/ \
           -v /tmp/output:/tmp/output \
           -it costrouc/pysrim sh -c "xvfb-run -a python3.6 /opt/pysrim/ni.py"
ls /tmp/output
```

This will start a docker container with a volume at `/opt/pysrim`
(with `ni.py` directory) and `/tmp/output` mounted in both the host
and src container for all srim output.

There is no loss of performance.
