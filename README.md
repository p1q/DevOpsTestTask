# DevOps Test Task

## Prerequisites

- Docker
- Docker Compose
- make
- curl
- jq
- helm
- kubectl
- kind

---

## How to Run (using Ubuntu Server as an example)

### 1. Install utilities
sudo apt update && sudo apt upgrade -y

sudo apt install -y docker.io

sudo usermod -aG docker $USER && newgrp docker

newgrp docker

sudo mkdir -p /usr/local/lib/docker/cli-plugins

sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose

sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose


sudo apt install -y make curl jq git

sudo apt install -y apt-transport-https curl



sudo snap install helm --classic

sudo snap install kubectl --classic


sudo curl -Lo /usr/local/bin/kind https://github.com/kubernetes-sigs/kind/releases/latest/download/kind-linux-amd64

sudo chmod +x /usr/local/bin/kind

### 2. Clone repository
sudo mkdir /DevOpsTestTask

sudo chown $(whoami):$(whoami) /DevOpsTestTask

git clone https://github.com/p1q/DevOpsTestTask.git

cd /DevOpsTestTask

### 3. Run Docker
make up

curl -s http://localhost:8080/healthz

make test

make logs

### _Expected Output:_
```bash
$ curl -s http://localhost:8080/healthz
{"status": "ok", "service": "app", "env": "local"}

$ make test
cp -n .env.example .env || true
curl -s http://localhost:8080/healthz | jq .
{
  "status": "ok",
  "service": "app",
  "env": "local"
}
Flood test (expect some 429s):
      6 200
     14 429

```

### 4. Run Kubernetes
kind create cluster --name devops --config k8s/kind-config.yaml

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx --namespace default --set controller.hostNetwork=true --set controller.hostPorts.http=80 --set controller.hostPorts.https=443 --set controller.kind=DaemonSet

docker build -t devops-test-app:latest ./app

kind load docker-image devops-test-app:latest --name devops

kubectl apply -f k8s/deployment.yaml

kubectl apply -f k8s/service.yaml

kubectl patch deployment app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","imagePullPolicy":"IfNotPresent"}]}}}}'

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout k8s/tls.key -out k8s/tls.crt -subj "/CN=localhost" -addext "subjectAltName=DNS:localhost"

kubectl create secret tls app-tls --cert=k8s/tls.crt --key=k8s/tls.key

kubectl apply -f k8s/ingress.yaml

kubectl get pods -w

curl -vk https://localhost/healthz

### _Expected Output:_
```bash
adm2@ubuntuv:/DevOpsTestTask$ curl -vk https://localhost/healthz
* Host localhost:443 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:443...
* connect to ::1 port 443 from ::1 port 60480 failed: Connection refused
*   Trying 127.0.0.1:443...
* Connected to localhost (127.0.0.1) port 443
* ALPN: curl offers h2,http/1.1
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 / X25519 / RSASSA-PSS
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=localhost
*  start date: Oct  1 16:56:30 2025 GMT
*  expire date: Oct  1 16:56:30 2026 GMT
*  issuer: CN=localhost
*  SSL certificate verify result: self-signed certificate (18), continuing anyway.
*   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://localhost/healthz
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: localhost]
* [HTTP/2] [1] [:path: /healthz]
* [HTTP/2] [1] [user-agent: curl/8.5.0]
* [HTTP/2] [1] [accept: */*]
> GET /healthz HTTP/2
> Host: localhost
> User-Agent: curl/8.5.0
> Accept: */*
>
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
< HTTP/2 200
< date: Wed, 01 Oct 2025 17:08:12 GMT
< content-type: application/json
< strict-transport-security: max-age=31536000; includeSubDomains
<
* Connection #0 to host localhost left intact
{"status": "ok", "service": "app", "env": "local"}
```
