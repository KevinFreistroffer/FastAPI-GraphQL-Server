fastapi run --reload --port 8000 --host 0.0.0.0                               

# Build the image
docker build -t fastapi-graphql .

# Run the container
docker run -p 8000:8000 -d fastapi-graphql