from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
 
def asset_preview_image_validator(image):
    dimensions = get_image_dimensions(image)
    if dimensions[0] < 720 or dimensions[1] < 923:
        raise ValidationError(f"Minimun width x height is 720x923px(yours - {dimensions[0]}X{dimensions[1]}px)")
    