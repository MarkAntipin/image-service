# image-service
Serve to serve images

## Run app
add .env file with the same variables as in .env.example

* `AWS_ACCESS_KEY_ID` - aws access key id; `required`
* `AWS_SECRET_ACCESS_KEY` - aws secret access key; `required`
* `REGION_NAME` - aws region name; `required`
* `BUCKET` - aws bucket name; `required`
* `ALLOWED_IMAGE_TYPES` - types of images that can be added; `default`: ["image/jpeg", "image/jpg", "image/png", "image/tiff"]
* `IMAGE_MIN_WIDTH` - minimal image width to request; `default`: 10
* `IMAGE_MIN_HEIGHT` - minimal image height to request; `default`: 10
* `IMAGE_MAX_WIDTH` - maximum image width to request; `default`: 2000
* `IMAGE_MAX_HEIGHT` - maximum image height to request; `default`: 2000

```bash
poetry install
poetry run python run.py
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
