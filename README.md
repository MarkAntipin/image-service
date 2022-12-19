# image-service
Serve to serve images

## Configuration
### Basic
* `IS_DEBUG` - enable debug logs; `default: 0`
* `STORAGE` - chose storage for your images ; `oneOf(s3, disk)`; `default: s3`
* `IMAGE_MIN_WIDTH` - minimal image width to request; `default: 10`
* `IMAGE_MIN_HEIGHT` - minimal image height to request; `default: 10`
* `IMAGE_MAX_WIDTH` - maximum image width to request; `default: 2000`
* `IMAGE_MAX_HEIGHT` - maximum image height to request; `default: 2000`
* `ALLOWED_IMAGE_TYPES` - types of images that can be added; `default: ["image/jpeg", "image/jpg", "image/png", "image/tiff"]`
* `IMAGE_PROCESSING_WORKERS` - number of processes to resize image; `default: 3`

### S3
`Only of you set STORAGE=s3`
* `S3_ACCESS_KEY_ID` - s3 access key id; `required`
* `S3_SECRET_ACCESS_KEY` - s3 secret access key; `required`
* `S3_REGION_NAME` - s3 region name
* `S3_BUCKET` - s3 bucket name; `required`
* `S3_ENDPOINT_URL` - s3 endpoint url; if you're using different from aws s3 storage, like minio


## Run app
add `.env` file in the project directory with the same variables as in `.env.example`

### With Docker
```bash
docker run --env-file .env -p 8080:8080 markantipin/image-service
```

### Without Docker
```bash
poetry install
poetry run uvicorn run:app --host 0.0.0.0 --port 8080 --workers 1
```

## API
docs available on ```http://0.0.0.0:8080/docs```

### Add Image
* **POST /api/v1/images**
```curl
curl -X 'POST' \
  'http://0.0.0.0:8080/api/v1/images' \
  -F 'file=@file.png;type=image/png'
```

### Get image
* **GET /api/v1/images/{image_id}**
```curl
curl -X 'GET' \
  'http://0.0.0.0:8080/api/v1/images/bc1794c9-2be2-4d46-98ef-fa6841f0b337' \
   -o file.jpg
```

### Get resized image
* **GET /api/v1/images/{width}x{height}/{image_id}**
```curl
curl -X 'GET' \
  'http://0.0.0.0:8080/api/v1/images/500x500/bc1794c9-2be2-4d46-98ef-fa6841f0b337' \
   -o file.jpg
```

## Development
**linters**:
```bash
poetry run flake8 .
poetry run isort -c .
```

**tests**:
```bash
poetry run coverage run -m pytest -v tests
poetry run coverage report -m --skip-empty --fail-under=90
```

**load tests**

Using [k6](https://k6.io)
```bash
k6 run load_tests/get_image.js
```
