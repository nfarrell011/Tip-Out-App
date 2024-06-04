import cv2
from pathlib import Path
import os

def create_iconset_from_png(source_image_path, output_directory):
    # Define the sizes for the icons
    icon_sizes = [16, 32, 64, 128, 256, 512, 1024]

    # Read the source image
    image = cv2.imread(source_image_path)
    if image is None:
        raise ValueError("Image could not be read. Check the file path.")

    # Ensure the output directory exists
    output_iconset_path = os.path.join(output_directory, 'output.iconset')
    os.makedirs(output_iconset_path, exist_ok = True)

    # Resize image and save each size
    for size in icon_sizes:
        resized_image = cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
        output_path = os.path.join(output_iconset_path, f"icon_{size}x{size}.png")
        cv2.imwrite(output_path, resized_image)
        print(f"Saved {output_path}")

# Usage
source_image = '/Users/nelsonfarrell/Documents/Northeastern/projects/tip_out_calc/figs/tip_out_app_icon.png'
output_dir = Path.cwd()  # Get current working directory
create_iconset_from_png(source_image, output_dir)

