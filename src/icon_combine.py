#!/usr/bin/env python3
import itertools
from pathlib import Path
from PIL import Image, ImageDraw

# ----------------------------------------------------------------------
# 1. CONFIGURATION
# ----------------------------------------------------------------------
ICON_SIZE = (50, 41)          # size to which every icon will be resized
CANVAS_SIZE = (400, 41)      # final image dimensions
GRID_ROWS, GRID_COLS = 1, 10   # layout grid (10 icons fit in 4×3)
BG_COLOR = (0, 0, 0, 255)     # black (opaque)
ICON_COLOR = (255, 255, 255, 255)  # white icons on black/transparent

# ----------------------------------------------------------------------
# 2. LOAD THE 10 ICON IMAGES (replace paths with your actual files)
# ----------------------------------------------------------------------
icon_paths = [
    "AC-Cafe-Shelf-Talkers_Allergens_Dairy.png",
    "AC-Cafe-Shelf-Talkers_Allergens_Egg.png",
    "AC-Cafe-Shelf-Talkers_Allergens_Gluten.png",
    "AC-Cafe-Shelf-Talkers_Allergens_Nut.png",
    "AC-Cafe-Shelf-Talkers_Allergens_Pork.png",
    "AC-Cafe-Shelf-Talkers_Allergens_Shrimp.png",
    "AC-Cafe-Shelf-Talkers_Allergens_Spice.png",
    "Gluten Free.png",
    "Vegan.png",
    "Vegetarian.png"
]

icons = []
for p in icon_paths:
    img = Image.open(p).convert("RGBA")
    img = img.resize(ICON_SIZE, Image.Resampling.LANCZOS)

    if p == "Gluten Free.png" or p == "AC-Cafe-Shelf-Talkers_Allergens_Gluten.png":
        # Crop the image to remove extra whitespace on the right side
        original_width, original_height = img.size
        new_width = 40  # desired width after cropping
        left = (original_width - new_width)
        right = (original_width)
        upper = 0
        lower = original_height

        # Ensure integer coordinates
        crop_box = (int(left), int(upper), int(right), int(lower))

        img = img.crop(crop_box)

    icons.append(img)

        

assert len(icons) == 10

# ----------------------------------------------------------------------
# 3. (NO LONGER NEEDED - positions computed dynamically per combination)
# ----------------------------------------------------------------------
# Positions are now calculated dynamically based on the number of active icons

# ----------------------------------------------------------------------
# 4. GENERATE ALL 2¹⁰ = 1024 COMBINATIONS
# ----------------------------------------------------------------------
output_dir = Path("icon_combinations")
output_dir.mkdir(exist_ok=True)

total = 1 << len(icons)   # 1024
for idx in range(total):
    canvas = Image.new("RGBA", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # which icons are active in this subset?
    active = [i for i in range(len(icons)) if (idx & (1 << i))]

    # Generate filename based on which icons are active
    # Each position in the string: 'X' if active, 'O' if not
    filename_code = ''.join('X' if (idx & (1 << i)) else 'O' for i in range(len(icons)))

    # right-align active icons
    num_active = len(active)
    if num_active > 0:
        # compute starting x position (right-aligned)
        total_width = num_active * ICON_SIZE[0]
        start_x = CANVAS_SIZE[0] - total_width
        y = (CANVAS_SIZE[1] - ICON_SIZE[1]) // 2  # center vertically
        
        for i, pos_idx in enumerate(active):
            icon_img = icons[pos_idx]
            x = start_x + i * ICON_SIZE[0]
            canvas.paste(icon_img, (x, y), icon_img)   # use alpha

    filename = output_dir / f"{filename_code}.png"
    canvas.save(filename, "PNG")

print(f"Generated {total} images in '{output_dir}'")
