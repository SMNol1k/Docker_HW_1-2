# Cборка Docker-container

## Сборка
docker image build . --tag=crud_docker_0.2

## Запуск контейнер
docker run -d -p 9090:8000 crud_docker_0.2