# Containerized HTTPS demo

Small **FastAPI** app in Docker, served over **HTTPS** with a **self-signed** certificate (local demo only).

## Run locally

1. Install [Docker](https://docs.docker.com/get-docker/) (with Compose).

2. Create TLS files (once):

   ```bash
   chmod +x scripts/gen-certs.sh
   ./scripts/gen-certs.sh
   ```

3. Start:

   ```bash
   docker compose up --build
   ```

4. Open **https://localhost/** — the browser will warn about the self-signed cert; proceed for local testing.

5. Check:

   ```bash
   curl -k https://localhost/health
   ```

## Design choices

- **One service** — Uvicorn handles HTTPS directly. Fewer parts than adding a separate reverse proxy, while still showing containers + TLS + mounted secrets.
- **Certificates on disk, mounted read-only** — the image has no key material; `certs/` is supplied at run time (demo certs can live in the repo for easy review, or you regenerate locally).
- **Python + FastAPI** — small dependency surface and clear handlers (`/` and `/health`).
- **Logging** — each request logs method, path, status, and duration to stdout (`docker compose logs -f web`).

## With more time

- Use a public CA or internal PKI instead of a committed self-signed key for anything beyond a laptop demo.
- Add Compose `healthcheck`, non-root user in the image, and image scanning in CI.
- Put real secrets in a cloud secret store, not in git.

## Tools / assistance

Standard **Docker**, **OpenSSL**, and framework docs only 

## Deploying to a cloud provider (e.g. AWS)

1. **Build** the image and push to a registry (**Amazon ECR**).
2. Run it on **ECS Fargate** or **EKS** (or **Lambda** + API Gateway if you refit to HTTP behind the gateway).
3. Terminate TLS at **Application Load Balancer** with **ACM** (certificate managed by AWS — private key not in your repo).
4. Send container logs to **CloudWatch**; inject config from **Secrets Manager** / **SSM** if needed.

Similar ideas on **Azure** (Container Apps + managed cert) or **GCP** (Cloud Run + HTTPS load balancer).

## Why a private SSL key should not live in a git repository

Anyone with repo access can copy the key and impersonate the service or decrypt traffic if TLS is misconfigured. Keys in git stay in **history** after rotation, backups and forks widen exposure, and repos are a poor place for rotation and access control compared to a **secrets manager** or **managed certificates** (e.g. ACM). Demo keys in a challenge repo are a deliberate exception for reviewers, not a production pattern.

## Layout

```
app/           # Application code
certs/         # Created by scripts/gen-certs.sh (demo)
scripts/       # gen-certs.sh
Dockerfile
docker-compose.yml
```
