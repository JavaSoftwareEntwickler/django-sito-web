from typing import Tuple
from PIL import Image


def get_new_image_dimensions( orig_dim: Tuple[int, int], new_width: int) -> Tuple[int, int]:
    original_width, original_height = orig_dim
    if original_width < new_width:
        return orig_dim
    aspect_ratio = original_height / original_width
    new_height = round(new_width * aspect_ratio)
    return (new_width, new_height)

def resize_image(original_image: Image, width: int) -> Image:
    image = Image.open(original_image)
    new_size = get_new_image_dimensions(image.size, width)
    if new_size == image.size:
        return
    
    return image.resize(new_size, Image.Resampling.LANCZOS)

