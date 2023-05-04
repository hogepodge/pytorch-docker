deploy-arm64: pytorch-arm64 notebook-pytorch-arm64 push-pytorch-arm64 push-notebook-pytorch-arm64

deploy-amd64: pytorch-amd64 notebook-pytorch-amd64 push-pytorch-amd64 push-notebook-pytorch-amd64

pytorch-arm64:
	docker build . -t hogepodge/pytorch:arm64-latest --build-arg ARCH=arm64

notebook-pytorch-arm64: pytorch-arm64
	docker build . -t hogepodge/notebook-pytorch:arm64-latest -f Dockerfile.notebook --build-arg ARCH=arm64

pytorch-amd64:
	docker build . -t hogepodge/pytorch:amd64-latest --build-arg ARCH=arm64

notebook-pytorch-x86: pytorch-amd64
	docker build . -t hogepodge/notebook-pytorch:amd64-latest -f Dockerfile.amd64 --build-arg ARCH=amd64

push-pytorch-arm64:
	docker push hogepodge/pytorch:arm64-latest

push-notebook-pytorch-arm64:
	docker push hogepodge/notebook-pytorch:arm64-latest

push-pytorch-amd64:
	docker push hogepodge/pytorch:amd64-latest

push-notebook-pytorch-amd64:
	docker push hogepodge/notebook-pytorch:amd64-latest

release-latest:
	docker manifest create \
        hogepodge/pytorch:latest \
        --amend hogepodge/pytorch:arm64-latest \
        --amend hogepodge/pytorch:amd64-latest
	docker manifest push hogepodge/pytorch:latest
	docker manifest create \
        hogepodge/notebook-pytorch:latest \
        --amend hogepodge/notebook-pytorch:arm64-latest \
        --amend hogepodge/notebook-pytorch:amd64-latest
	docker manifest push hogepodge/notebook-pytorch:latest

mlbackend-arm64: pytorch-arm64
	docker build . -t hogepodge/mlbackend:latest -f Dockerfile.ls_ml --build-arg ARCH=arm64

run-mlbackend-arm64: mlbackend-arm64
	docker run --rm -p 9090:9090 -v $(PWD)/work:/home/pytorch/work --name mlbackend hogepodge/mlbackend:latest 
