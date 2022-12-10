https://docs.docker.com/engine/swarm/stack-deploy/

docker-compose up -d
docker-compose push
docker stack deploy --compose-file docker-compose.yml ucla_ssh

 docker stack rm ucla_ssh

test hook
