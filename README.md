To use the latest build of these images:

```docker pull hogepodge/pytorch:latest
docker pull hogepodge/notebook-pytorch:latest
```
Run with a sentiment analysis tutorial:
```
git clone https://github.com/bentrevett/pytorch-sentiment-analysis
docker run --rm -p 8888:8888 -v $(HOME)/pytorch-sentiment-analysis:/home/pytorch/work hogepodge/notebook-pytorch:latest
```

To run the Label Studio ML Backend:
```
git clone https://github.com/hogepodge/pytorch-docker.git
cd pytorch-docker
make run-mlbackend-arm64
```

You can replace the `work/model.py` with your own model following the Label Studio model interface.
