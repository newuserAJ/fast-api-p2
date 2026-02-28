from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

image_kit = ImageKit(
    public_key=os.getenv("PUBLIC_KEY"),
    private_key=os.getenv("PRIVATE_KEY"),
    url_endpoint=os.getenv("IMAGEKIT_URL"),
)