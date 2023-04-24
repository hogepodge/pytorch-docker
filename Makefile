all: pytorch notebook-pytorch

push: push-pytorch push-notebook-pytorch

pytorch:
	docker build . -t hogepodge/pytorch:latest

notebook-pytorch: pytorch
	docker build . -t hogepodge/notebook-pytorch:latest -f Dockerfile.notebook

notebook-pytorch-x86: pytorch
	docker build . -t hogepodge/notebook-pytorch:latest -f Dockerfile.x86

push-pytorch:
	docker push hogepodge/pytorch:latest

push-notebook-pytorch:
	docker push hogepodge/notebook-pytorch:latest
