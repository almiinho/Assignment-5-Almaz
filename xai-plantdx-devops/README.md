# XAI-PlantDx DevOps Sample
Student: Azamatov Almaz — CSE-2506 | Applied Software Development

This project packages the Assignment 3 dataset-audit utility as a reproducible component of XAI-PlantDx, the plant disease classification project carried through Assignments 1–4. It checks dataset folder structure and emits JSON; it does not train or diagnose a model.

## CI pipeline
Jenkins checks out the repository, installs the package, runs unit tests, builds a Docker image and performs a container smoke test. GitHub Actions separately runs unit tests on pushes and pull requests.

## Local run
```bash
python -m pip install -e .
python -m pip install -r requirements-dev.txt
python -m pytest -v
plant-dataset-audit path/to/dataset --output reports/audit.json
```

## Docker
```bash
docker build -t xai-plantdx-dataset-audit:local .
docker run --rm xai-plantdx-dataset-audit:local --help
```

## Start Jenkins locally
Prerequisites: Docker Engine and Docker Compose plugin.
```bash
docker compose -f docker-compose.jenkins.yml up -d
docker exec xai-plantdx-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Open `http://localhost:8080`, complete setup, install Pipeline and Git plugins, then create a Pipeline job configured as “Pipeline script from SCM”. Set the repository URL, branch and Script Path `Jenkinsfile`, then select “Build Now”.

The Jenkins container requires Docker CLI/daemon access for image-building stages. The Compose file mounts the host Docker socket, which grants powerful host access. Use only on a trusted local machine; a dedicated Jenkins agent is safer for shared environments.

## GitHub publication
Create a public repository named `xai-plantdx-devops`, push these files, and verify Actions. Do not claim a remote repository or Jenkins run exists until those steps are complete.

## Limitations
Tests use temporary placeholder files, not the full plant dataset. Repeated filenames are a heuristic, not proof of identical image content. The Docker/Jenkins configuration is prepared but must be run in your environment.
