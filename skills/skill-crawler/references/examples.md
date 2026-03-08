# Example Skills

Complete example skills demonstrating best practices.

## Docker CLI Example

```markdown
---
name: docker-cli
version: "1.0.0"
description: Automate Docker containers for building, running, and deploying. Use when working with Dockerfiles, images, containers, or Docker Compose.
metadata:
  source_url: https://github.com/benjaminwestern/google-engineer-skills
---

# Docker CLI

## Quick Start

```bash
docker run -d -p 80:80 nginx
docker build -t myapp .
docker compose up -d
```

## Commands

### Containers

```bash
docker run -d --name mycontainer nginx
docker ps
docker logs mycontainer
docker stop mycontainer
docker rm mycontainer
```

### Images

```bash
docker build -t myimage .
docker images
docker push registry/myimage
docker pull nginx
```

## Examples

### Build and Run a Container

```bash
# Build from Dockerfile
docker build -t myapp:latest .

# Run container
docker run -d -p 8080:80 --name myapp myapp:latest

# View logs
docker logs -f myapp
```

### Cleanup

```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune
```

## Tips

- Use `--rm` for temporary containers
- Use `-v` for persistent data
- Use `--network` for container communication

```

## Key Characteristics

This example demonstrates:

1. **Clear Description**: Specific use cases and context
2. **Quick Start**: 3 essential commands covering 80% of use cases
3. **Organized Commands**: Grouped by functionality
4. **Complete Examples**: Full command sequences, not snippets
5. **Practical Tips**: Actionable best practices

## More Examples

See the [skills directory](../..) for additional production-ready examples:

- `tech-writer` - Documentation generation
- `terraform` - Infrastructure as code
- `google-adk` - AI agent development
