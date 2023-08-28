# Тестовое задание для поступления в DevOps Cloud.ru Camp

Результаты выполнения тестового задания следует опубликовать на GitHub или захостить на любой открытой платформе (например, Github Pages) и отправить на почту <devopscloudcamp@cloud.ru>. Также следует указать свои контактные данные для получения обратной связи.

## 1. Ansible playbook

### How to setup ansible.cfg and launch your playbook

* Add the `your private key` to the directory you need
* Specify it in the `your_repo/ansible.cfg` file under the `private_key_file` option.
* Set the `inventory` file in the `inventory` option.
* Run the command `ansible-playbook playbook.yml` in directory `your_repo/playbook`.

### How to fast check ansible playbook if you don't have inventory

To fast check playbook i used Vagrant

Execute next commands:

```bash
cd ~/your_repo/playbook
vagrant up
```

After starting the virtual machine, you will see the execution of the playbook with the keys that vagrant creates for his needs.
You should see next output

```bash
PLAY RECAP *********************************************************************
tag_cloud                  : ok=7    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

After this you can check idempotence:

```bash
vagrant provision tag_cloud
```

expected result:

```bash
PLAY RECAP *********************************************************************
tag_cloud                  : ok=5    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

You also can use inventory from vagrant inventory file in directory `your_repo/playbook/.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory` to set up your `ansible.cfg` and test `ansible-playbook playbook.yml` command

However, for optimal idempotency testing, it's advisable to use specialized tools like `Molecule`.

## 2. Web application on Python

* A Python script has been created using `Fastapi` to assign endpoints.
* Created endpoints:
    `/id`
    `/hostname`
    `/author`
    `readiness`
    `liveness`
* A dependency file `requirements.txt` has been created for launching applications

### How to setup application

setup dependecies

```bash
cd ~/your_repo/app
pip install --upgrade -r requirements.txt
```

After launch your app

```bash
AUTHOR=some_name UUID=some_valid_uuid_v4_or_not_valid_to_check_readiness_probe  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### How to check application

```bash
curl http://localhost:8000/created_endpoints
```

## 3. Dockerfile

A Dockerfile was created in the `your_repo/app` directory. To create it was used:

* Images are based on alpine.
* Specific versions of base images are pinned during the build.
* Dependencies in the `requirements.txt` file are pinned to specific versions required for the application's execution.
* Multi-stage build is employed.
* Layers that are likely to change frequently, such as app source code, are positioned towards the end of the Dockerfile.
* The final image is created as `rootless`.

I am aware of the existence of distroless images, <https://github.com/GoogleContainerTools/distroless> but the documentation separately states:

```text
The following images are also published on gcr.io, but are considered experimental and not recommended for production usage:
gcr.io/distroless/python3-debian11
```

As a result, I chose not to utilize it.

I also chose not to set a default value for the environment variable UUID, because it's challenging for people to comprehend and remember entries like `54015250-c765-48a3-9921-6bc47bb40e11`. If you happen to forget to specify this variable in a Kubernetes Deployment, your application will fail the readiness check. But if you have a default value set, this might go unnoticed.

### How to create docker image

To create the final image, run the following commands:

```bash
cd ~/your_repo/app
docker build -t your_hub_name/image_name:tag .
# If necessary, push to your custom Docker registry or Docker Hub
docker push your_hub_name/image_name:tag
```

### How to check your image

To test your image, run the following commands:

```bash
# You can try different scenarios by passing a valid or invalid UUID to the variable.
docker run -e UUID=some_valid_or_not_UUID -d -p 8000:8000 your_hub_name/image_name:tag

curl http://localhost:8000/endpoints_in_app
```

## Kubernetes manifest

* A `deployment.yml` manifest has been created, which sets up the namespace `cloudru` and the deployment itself.
* A `service.yml` manifest with a ClusterIP type has been created to serve the deployment.

The deployment has 3 replicas. The `UUID` variable is assigned the value of `meta.uid` during the deployment rollout. This variable is used in the `readiness` probe within the application code. The `AUTHOR` variable is also used for the `readiness` probe validation, ensuring you didn't forget to set the variable in the Dockerfile.

### How to rollout your deployment

If you don't have kubernetes cluster use minikube

```bash
minikube start  --kubernetes-version=v1.26.3
```

rollout your deployment

```bash
cd ~/your_repo/manifest
kubectl apply -f ./
```

### How to check your deploy

Check readiness your pods and your service

```bash
kubectl get pod -n your_namespace
kubectl get svc -n your_namespace
# or inspect events to catch errors
watch kubectl events -n your_namespace
# or inspect pod logs
kubectl logs pod_name -n your_namespace --watch
```

Check working your app

```bash
kubectl port-forward your_pod_name 8000:8000
# open new terminal
curl http://localhost:8000/endpoints
```

## Helm chart

In the `/helm` directory, a chart has been created that sets up a deployment and a service for it, as well as a `README.md` file generated using the `helm-docs` utility.

### How to setup and deploy helm chart

```bash
cd ~/your_repo/helm
# Ensure your manifests are correctly generated
helm template .
# Deploy
helm upgrade --install your_release_name . --namespace your_namespace --create-namespace
```

### How to check your deployed chart

```bash
# Check created service name
kubectl get svc -n your_namespace
# Launch pod with curl and sh/bash/etc
kubectl run pod_name --image image_with_curl_and_sh -n your_namespace
k exec -it debug -n your_namespace -- sh
# within container check your app endpoints
curl http://service_name:8000/endpoints
```
Endpoints such as `/id` `/hostname` can be checked several times in a row to ensure that your service is load balancing between different pods, and you can receive a different `UUID` and `/hostname` from each pod.
