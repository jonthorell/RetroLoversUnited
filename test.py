import os
import env
import dj_database_url

value = os.getenv("CLOUDINARY_URL")

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

print(DATABASES)