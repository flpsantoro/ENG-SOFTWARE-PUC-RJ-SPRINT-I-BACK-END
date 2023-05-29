#! /bin/sh

git pull origin

rm -R /srv/api_sprint_i/
mkdir /srv/api_sprint_i/

cd api || ! echo "FALHA! Pasta não encontrada"

docker network create puc
docker ps -a | awk '{ print $1,$2 }' | grep flpsantoro/api_sprint_i:1.0 | awk '{print $1 }' | xargs -I {} docker rm -f {}
docker rmi flpsantoro/api_sprint_i:1.0
docker build --tag=flpsantoro/api_sprint_i:1.0 --rm=true .

docker run  \
  --name api_sprint_i \
  --hostname=api_sprint_i \
  -p 33002:5000 \
  --network=puc \
  -d flpsantoro/api_sprint_i:1.0

echo "Iniciando Aplicação..."

docker exec api_sprint_i python /app/app.py


echo "Deploy concluído">nome.txt