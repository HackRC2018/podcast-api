# Installation
```
python3 -m venv .env && source .env/bin/activate
pip install -r requirements.txt

MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=podcast
```

# Docker
```
# building
docker build -t podcast-api .

# start mongo
docker run --name podcast-mongo -d mongo

# run api
docker run -d \
    -p 5000:5000 \
    --name podcast-api \
    --link podcast-mongo:mongo \
    -e 'MONGODB_HOST=mongo' \
    podcast-api
```

# Push and Pull image
```
# Push to Docker Hub
docker tag podcast-api william57m/podcast-api
docker push william57m/podcast-api

# Pull in Azure
docker pull william57m/podcast-api
```
