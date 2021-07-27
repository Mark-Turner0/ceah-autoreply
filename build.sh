docker stop ceah-autoreply
docker rm ceah-autoreply
docker rmi -f ceah-autoreply
docker build -t ceah-autoreply ./ --no-cache

