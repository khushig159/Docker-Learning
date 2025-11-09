
# Dockerized Full-Stack Application (Node.js + Python + MySQL)

This repository contains a **full-stack Dockerized application** with:
- A **Node.js frontend** (Vite dev server running on port `5173`)
- A **Python backend** (interacting with MySQL via `pymysql`)
- **MySQL database** (running in a container)
- **Docker networking** and **volume mounting** for persistence and communication

Everything is containerized using **Docker**, allowing consistent, isolated, and reproducible environments.

---

## Docker Concepts Explained

Before diving into the code and commands, here are the **core Docker terms** used in this project:

| Term | Explanation |
|------|-----------|
| **`Container`** | A lightweight, isolated runtime environment that runs your app with its dependencies. Think of it as a mini-VM, but faster and more efficient. |
| **`Image`** | A read-only template (like a blueprint) used to create containers. Built from a `Dockerfile`. |
| **`Dockerfile`** | A text file with instructions to build a Docker image (e.g., install packages, copy files, set commands). |
| **`docker build`** | Command to create an image from a `Dockerfile`. |
| **`docker run`** | Starts a new container from an image. |
| **`-p <host>:<container>`** | Maps a port on your machine to a port inside the container (e.g., `-p 5173:5173`). |
| **`-d`** | Runs container in **detached mode** (in the background). |
| **`--rm`** | Automatically removes the container when it stops. Great for testing. |
| **`--name`** | Gives the container a custom name (e.g., `mywebapp`). |
| **`-it`** | Runs container in **interactive mode** with a terminal (`-i`) and pseudo-TTY (`-t`). |
| **`-v <host-path>:<container-path>`** | **Volume mount** — binds a file/folder from your machine into the container for persistence or live editing. |
| **`docker ps`** | Lists **running** containers. |
| **`docker ps -a`** | Lists **all** containers (running + stopped). |
| **`docker stop <name>`** | Gracefully stops a running container. |
| **`docker rm <name>`** | Removes a stopped container. |
| **`docker rmi <image>`** | Removes a Docker image. |
| **`docker images`** | Lists all local images. |
| **`docker network`** | Allows containers to communicate with each other securely and efficiently. |
| **`docker volume`** | Persistent storage that lives outside containers. Data survives container restarts/removal. |


---

## Dockerfiles Explained

### 1. `docker-client/Dockerfile` (Node.js Frontend)

```dockerfile
FROM node:20-alpine
```
- **`FROM`**: Starts with the official **Node.js 20** image based on lightweight **Alpine Linux**.

```dockerfile
WORKDIR /docker-client
```
- **`WORKDIR`**: Sets the working directory inside the container to `/docker-client`. All future commands run here.

```dockerfile
COPY . .
```
- **`COPY`**: Copies **all files** from the current directory (on host) into the container's working directory.

```dockerfile
RUN npm install
```
- **`RUN`**: Executes a command **during image build**. Installs Node.js dependencies.

```dockerfile
CMD ["npm", "run", "dev"]
```
- **`CMD`**: Default command to run when the container starts. Starts Vite dev server.

---

### 2. `python/Dockerfile` (Python Backend)

```dockerfile
FROM python
```
- **`FROM`**: Uses the official **Python** base image.

```dockerfile
WORKDIR /python
```
- **`WORKDIR`**: Sets working directory to `/python`.

```dockerfile
COPY ./sqldemo.py .
```
- **`COPY`**: Copies only `sqldemo.py` into the container (efficient for small apps).

```dockerfile
RUN pip install pymysql
RUN pip install cryptography
```
- **`RUN`**: Installs required Python packages during build.

```dockerfile
CMD ["python", "sqldemo.py"]
```
- **`CMD`**: Runs the Python script when container starts.

---

## Key Docker Commands (Generalized & Explained)

> Only **important and new** Docker commands are explained below.

### Building Images

```bash
docker build -t <name>:<tag> .
```

| Part | Meaning |
|------|--------|
| `docker build` | Build an image from `Dockerfile` in current directory |
| `-t name:tag` | Tags the image (e.g., `docker-client:03`) |
| `.` | Build context = current directory |

**Use in development**: Version your images, avoid conflicts, easy to reference.

---

### Running Containers

```bash
docker run -d --rm --name myapp -p 5173:5173 image-name
```

| Flag | Purpose |
|------|--------|
| `-d` | Run in background |
| `--rm` | Auto-delete container on exit |
| `--name` | Custom container name |
| `-p 5173:5173` | Map host port → container port |

**Use**: Clean, isolated runs without leftover containers.

---

### Interactive Mode

```bash
docker run -it --rm image-id
```

- `-it` → Opens a **shell inside the container**
- Useful for **debugging**, testing scripts, or database access

---

### Volume Mounting

```bash
docker run -v "/host/path/file.txt:/container/path/file.txt" --rm image
```

**Example**:
```bash
docker run -v "C:/Users/.../server.txt:/python/server.txt" --rm my-python-app
```

**Why use volumes?**
- Edit files on host → instantly reflect in container
- Share config/data between host and container
- Persist logs, credentials, or input files

---

### Docker Volumes (Named)

```bash
docker volume create myvolume
docker run -v myvolume:/myapp --rm image
```

**Benefits**:
- Data persists even if container is deleted
- Better than bind mounts for database storage
- Managed by Docker

---

## Docker Networking

Docker **networks** enable secure, reliable communication between containers. This is essential for full-stack apps where services (frontend, backend, database) must talk to each other.

---

### Create a Custom Network

```bash
docker network create mynet

### This creates an isolated network called `mynet`.

### Run Containers on the Same Network

```bash
# MySQL container
docker run -d \
  --name mysqldb \
  --network mynet \
  -e MYSQL_ROOT_PASSWORD="root" \
  -e MYSQL_DATABASE="userinfo" \
  mysql:latest

# Python app (connects to MySQL)
docker run -it --rm \
  --network mynet \
  --name mypythonapp \
  my-python-image
```

### Why Use Docker Networks?

| Benefit | Explanation |
|--------|-------------|
| **Name-based resolution** | Use `mysqldb` as hostname — no IP needed |
| **Isolation** | Only containers on `mynet` can see each other |
| **No internal port mapping** | Backend connects directly via container name |
| **IP changes don’t break app** | Docker DNS handles resolution |

---

### In Python Code: Use Container Name as Host

```python
import pymysql

return pymysql.connect(
    host="mysqldb",        # Container name = hostname
    user="root",
    password="root",
    database="userinfo"
)
```

**Works because**:
- Docker’s built-in DNS resolves `mysqldb` → current IP of MySQL container
- Survives container restarts
- Clean, portable, production-ready

---

### Without a Network (Not Recommended)

If containers are on the **default bridge**, they **cannot** resolve names.

#### Step 1: Get MySQL IP

```bash
docker inspect mysqldb | grep IPAddress
```

Example output:
```json
"IPAddress": "172.17.0.2"
```

#### Step 2: Hardcode IP in Code

```python
host="172.17.0.2"  # Fragile — breaks on restart
```

**Problems**:
- IP changes when container restarts
- Not portable across machines
- Hard to maintain

---

### Network vs No Network

| Approach | Host in Code | Reliable? | Portable? | Recommended? |
|--------|--------------|---------|----------|--------------|
| **With `mynet`** | `host="mysqldb"` | Yes | Yes | **YES** |
| **No network** | `host="172.17.0.2"` | No | No | No |

---

### Special Case: `host.docker.internal`

```python
host="host.docker.internal"  # Only works on Docker Desktop
```

**Use only** to connect from container → **host machine services** (e.g., local DB).  
**Never use in production**.

---

### MySQL Environment Variables

| Variable | Purpose |
|--------|--------|
| `MYSQL_ROOT_PASSWORD` | Sets root password |
| `MYSQL_DATABASE` | Auto-creates database on first run |

**Tip**: Always combine `--network`, `--name`, and `-e` flags for secure, connected services.

---

**Best Practice**  
> **Always use a custom network. Never hardcode IPs. Use container names as hostnames.**


---

## Managing Containers & Images

| Command | Purpose |
|--------|--------|
| `docker ps` | See running containers |
| `docker ps -a` | See all (including stopped) |
| `docker stop <name>` | Stop gracefully |
| `docker rm <name>` | Remove stopped container |
| `docker rmi <image>` | Delete image |
| `docker image ls` | List images |
| `docker volume ls` | List volumes |

**Best Practice**: Clean up unused containers/images regularly.

---

## Development Workflow Summary

1. **Edit code locally**
2. **Rebuild image** → `docker build -t app:latest .`
3. **Run with live reload** (Node.js) or volume mount (Python)
4. **Use networks** to connect services
5. **Use volumes** for persistent data or file sharing

---

## Cleanup Commands

```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker rm $(docker ps -a -q)

# Remove unused images
docker rmi $(docker images -q -f dangling=true)

# Remove specific image
docker rmi my-app:01
```
---

## Docker Compose: Orchestrate Multi-Container Apps

### What is Docker Compose?

**Docker Compose** is a tool that lets you define and run **multi-container Docker applications** using a single `docker-compose.yml` file.

Instead of running multiple `docker run` commands manually, you define:
- All services (containers)
- Networks
- Volumes
- Dependencies
- Health checks

Then start everything with **one command**.

---

### Why Use Docker Compose?

| Benefit | Explanation |
|--------|-------------|
| **Single source of truth** | All config in one `docker-compose.yml` file |
| **Easy startup/shutdown** | `docker-compose up` / `down` |
| **Automatic networking** | Services can talk using **service names** |
| **Dependency management** | `depends_on` waits for DB to be ready |
| **Consistent environments** | Same setup on dev, CI, staging |
| **Reproducible** | Share `.yml` → everyone gets identical stack |

---

## `docker-compose.yml` Explained

We have **two files**:

1. `python/docker-compose.yml` → Python + MySQL  
2. `docker-client/docker-compose.yml` → Node.js frontend

---

### 1. `python/docker-compose.yml` (Backend + DB)

```yaml
services:
  mysqldb:
    image: 'mysql:latest'
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=userinfo
    container_name: "mysqldb"
    healthcheck:
      test: ["CMD", "mysqladmin","ping","-h","localhost"]
      timeout: 20s
      retries: 10
    networks: 
      - mynetwork

  mypythonapp:
    build: ./
    container_name: mypyapp
    networks:
      - mynetwork
    volumes:
      - ./server.txt:/python/server.txt  # bind mount
    depends_on:
      mysqldb:
        condition: service_healthy
    stdin_open: true
    tty: true 

networks:
  mynetwork:
```

---

#### Service: `mysqldb`

| Key | Purpose |
|-----|--------|
| `image: mysql:latest` | Use official MySQL image |
| `environment` | Set root password & auto-create DB |
| `container_name` | Fixed name: `mysqldb` |
| `healthcheck` | Ensures DB is ready before app starts |
| `networks` | Joins custom network |

---

#### Service: `mypythonapp`

| Key | Purpose |
|-----|--------|
| `build: ./` | Build from local `Dockerfile` |
| `container_name` | Name: `mypyapp` |
| `volumes` | Mount `server.txt` from host → container |
| `depends_on` + `service_healthy` | **Wait** until MySQL is healthy |
| `stdin_open: true`, `tty: true` | Enable interactive mode (`-it`) |

---

#### Network

```yaml
networks:
  mynetwork:
```

- Auto-created if not exists
- Both services can reach each other via **service name** (`mysqldb`)

---

### 2. `docker-client/docker-compose.yml` (Frontend)

```yaml
services:
  mywebapp:
    build: ./
    ports: 
      - 5173:5173
    container_name: mywebapp
```

| Key | Purpose |
|-----|--------|
| `build: ./` | Build from local Node.js `Dockerfile` |
| `ports` | Map host port `5173` → container `5173` |
| `container_name` | Fixed name: `mywebapp` |

> Open [http://localhost:5173](http://localhost:5173) to see the app.

---

## Docker Compose Commands

| Command | What It Does |
|--------|--------------|
| `docker-compose up` | Build (if needed) + start all services |
| `docker-compose up -d` | Run in **detached mode** (background) |
| `docker-compose down` | Stop and **remove** containers + network |
| `docker-compose down -v` | Also remove **volumes** |
| `docker-compose logs` | View logs from all services |
| `docker-compose ps` | List running services |
| `docker-compose exec mypythonapp bash` | Open shell inside container |

---

## Full Workflow

### In `python/` directory:
```bash
docker-compose up
```
→ Starts MySQL → waits for health → starts Python app

### In `docker-client/` directory:
```bash
docker-compose up -d
```
→ Starts Node.js dev server at `http://localhost:5173`

---

## Connection in Python (No IP Needed!)

```python
pymysql.connect(
    host="mysqldb",    # Service name from docker-compose
    user="root",
    password="root",
    database="userinfo"
)
```

Docker Compose **automatically** sets up DNS — just use the **service name**.

---

## Cleanup

```bash
# In each directory
docker-compose down        # Stop + remove containers
docker-compose down -v     # Also remove volumes
```

---

**Pro Tip**: Use `docker-compose.yml` for **local development**, **testing**, and **CI**. It replaces 10+ `docker run` commands with **one file + one command**.

---

**Now your entire stack is portable, reliable, and easy to share.**

---

## Real-Life Scenarios: Where Docker Shines for Developers

Docker isn't just a tool — it's a **game-changer** in modern software development. Here are **real-world use cases** every developer faces, and how Docker solves them **cleanly and efficiently**.

---

### 1. **"It Works on My Machine" Syndrome**
> **Problem**: App runs on your laptop but fails on a teammate’s machine or in production.  
> **Cause**: Different OS, Python/Node versions, missing libraries, config drift.

**Docker Fix**:
```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["3000:3000"]
```
- Same image runs **everywhere** — dev, CI, staging, prod  
- No more "But it works locally!" excuses

---

### 2. **Multiple Projects, Conflicting Dependencies**
> **Problem**:  
> - Project A needs **Python 3.9**  
> - Project B needs **Python 3.11**  
> - Node.js 16 vs 20  
> → Global installs break everything

**Docker Fix**:
```dockerfile
# Project A
FROM python:3.9
# Project B
FROM python:3.11
```
- Run **10 projects** on one machine  
- Zero conflicts  
- Clean teardown with `docker rm`

---

### 3. **Onboarding New Developers**
> **Problem**: New hire spends **2 days** setting up environment  
> → Install MySQL, Redis, Node, Python, env vars, SSL certs…

**Docker Fix**:
```bash
git clone repo.git
cd repo
docker-compose up
```
**Done in 2 minutes**  
No manuals. No "Did you install X?"

---

### 4. **Testing with Real Dependencies**
> **Problem**: Unit tests pass, but integration fails in staging  
> → "We don’t have Kafka locally"

**Docker Fix**:
```yaml
services:
  app:
    build: .
    depends_on: [mysql, redis, kafka]
  mysql:
    image: mysql:8
  redis:
    image: redis:alpine
  kafka:
    image: confluentinc/cp-kafka
```
- Spin up **full stack** locally  
- Test against **real services**, not mocks

---

### 5. **CI/CD Pipeline Reliability**
> **Problem**: Build passes in Jenkins, fails in GitLab CI  
> → Different base images, cached packages

**Docker Fix**:
```yaml
# .github/workflows/ci.yml
- name: Build & Test
  run: docker-compose -f docker-compose.test.yml up --build --exit-code-from app
```
- **Same image** in every runner  
- No caching issues  
- Fast, isolated, reproducible

---

### 6. **Microservices Development**
> **Problem**: 15 services → 15 terminals → chaos

**Docker Fix**:
```yaml
services:
  auth-service:
    build: ./auth
    ports: ["4000:4000"]
  user-service:
    build: ./user
    depends_on: [db]
  api-gateway:
    build: ./gateway
```
```bash
docker-compose up
```
- All services up in **one command**  
- Auto-networking: `user-service` → `http://auth-service:4000`

---

### 7. **Database Migrations & Seeding**
> **Problem**: "I forgot to run the migration script!"

**Docker Fix**:
```yaml
services:
  db:
    image: postgres
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
```
- DB auto-initialized on first run  
- Same schema everywhere

---

### 8. **Hot Reloading in Development**
> **Problem**: Edit code → rebuild → restart → slow feedback

**Docker Fix** (Node.js + Vite):
```yaml
services:
  web:
    build: .
    volumes:
      - .:/docker-client
      - /docker-client/node_modules
    ports: ["5173:5173"]
```
- Edit `App.jsx` → **instant reload** in browser  
- No rebuild needed

---

### 9. **Production-like Local Environment**
> **Problem**: Local uses SQLite, prod uses MySQL → bugs in production

**Docker Fix**:
```yaml
services:
  db:
    image: mysql:8.0  # Same as production
    environment:
      MYSQL_ROOT_PASSWORD: root
```
- Test with **exact same DB engine, version, config**

---

### 10. **Demo & Client Presentations**
> **Problem**: Client says "Can you show it now?"  
> → Your laptop is offline, or setup breaks

**Docker Fix**:
```bash
docker pull yourname/demo-app:latest
docker run -p 8080:80 yourname/demo-app
```
- Ship a **single image**  
- Runs anywhere with Docker  
- No setup. Just `docker run`

---

## Summary: Docker in a Developer’s Life

| Scenario | Without Docker | With Docker |
|--------|----------------|------------|
| Setup time | Hours/Days | **Minutes** |
| Environment parity | Never | **Always** |
| Team sync | Manual docs | `docker-compose up` |
| Debugging | "It works here" | Reproducible |
| Deploy confidence | Low | **High** |

---

**Docker doesn’t just containerize apps — it containerizes chaos.**

> **Use Docker = Ship faster. Break less. Sleep better.**

**Made with ❤️ for reproducible, portable development**
