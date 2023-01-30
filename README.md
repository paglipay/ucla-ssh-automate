https://docs.docker.com/engine/swarm/stack-deploy/

docker-compose up -d
docker-compose push
docker stack deploy --compose-file docker-compose.yml ucla_ssh

 docker stack rm ucla_ssh

pyinstaller --onefile --windowed --console --paths ..\\venv\\Lib\\site-packages --hidden-import paramiko --hidden-import requests --hidden-import serial --hidden-import subprocess app.py
