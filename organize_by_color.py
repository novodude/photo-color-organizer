import os
import shutil
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import random

# Color name lists for renaming
COLOR_NAMES = {
    "Red": [
        "ruby",
        "crimson",
        "scarlet",
        "cherry",
        "rose",
        "cardinal",
        "coral",
        "vermillion",
    ],
    "Dark_Red": ["burgundy", "wine", "maroon", "mahogany", "brick", "rust"],
    "Orange": ["tangerine", "apricot", "peach", "amber", "copper", "sunset"],
    "Dark_Orange": ["terracotta", "burnt_orange", "pumpkin", "clay"],
    "Yellow": ["lemon", "gold", "sunshine", "butter", "canary", "daffodil", "honey"],
    "Gold": ["golden", "brass", "bronze", "mustard"],
    "Yellow_Green": ["lime", "chartreuse", "olive", "pistachio"],
    "Green": ["emerald", "jade", "forest", "grass", "mint", "sage", "fern"],
    "Dark_Green": ["hunter", "pine", "moss", "jungle", "ivy"],
    "Teal": ["turquoise", "aquamarine", "seafoam", "ocean"],
    "Cyan": ["sky", "ice", "azure", "arctic", "lagoon"],
    "Blue": ["sapphire", "cobalt", "cerulean", "marine", "royal", "azure_blue"],
    "Dark_Blue": ["navy", "midnight", "indigo", "denim", "steel"],
    "Purple": ["violet", "lavender", "orchid", "amethyst", "plum", "lilac"],
    "Dark_Purple": ["eggplant", "grape", "aubergine", "mulberry"],
    "Magenta": ["fuchsia", "hot_pink", "neon_pink", "electric"],
    "Pink": ["rose_pink", "blush", "salmon", "carnation", "flamingo", "bubblegum"],
    "Brown": ["chocolate", "coffee", "cocoa", "chestnut", "walnut", "espresso"],
    "Tan": ["sand", "camel", "khaki", "wheat", "biscuit"],
    "Beige": ["cream", "ivory", "ecru", "linen", "vanilla"],
    "White": ["pearl", "snow", "cloud", "milk", "alabaster"],
    "Light_Gray": ["silver", "platinum", "ash", "dove"],
    "Gray": ["slate", "pewter", "charcoal_gray", "stone"],
    "Dark_Gray": ["graphite", "charcoal", "iron", "smoke"],
    "Mixed": ["rainbow", "multicolor", "mosaic", "spectrum", "prism"],
}


def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV color space."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c

    if max_c == min_c:
        h = 0
    elif max_c == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_c == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360

    s = 0 if max_c == 0 else (diff / max_c)
    v = max_c

    return h, s, v


def get_dominant_colors(image_path, n_colors=5):
    """Extract dominant colors using K-means clustering (pywal-style)."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")

        # Resize for faster processing
        img.thumbnail((200, 200))

        # Convert to numpy array
        img_array = np.array(img)
        pixels = img_array.reshape(-1, 3)

        # Remove very dark pixels (often background/borders)
        mask = np.sum(pixels, axis=1) > 30
        pixels = pixels[mask]

        if len(pixels) < 10:
            return None

        # Use K-means to find dominant colors
        n_clusters = min(n_colors, len(pixels))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(pixels)

        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)

        # Count pixels in each cluster
        labels = kmeans.labels_
        counts = np.bincount(labels)

        # Sort by frequency
        indices = np.argsort(-counts)
        dominant_color = colors[indices[0]]

        return tuple(dominant_color)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def classify_color(rgb):
    """Classify RGB values using HSV color space for better accuracy."""
    r, g, b = rgb
    h, s, v = rgb_to_hsv(r, g, b)

    # Normalize values
    brightness = v * 255
    saturation = s

    # Grayscale detection (low saturation)
    if saturation < 0.15:
        if brightness > 220:
            return "White"
        elif brightness > 170:
            return "Light_Gray"
        elif brightness > 100:
            return "Gray"
        else:
            return "Dark_Gray"

    # Color classification based on hue
    # Red: 0-15, 345-360
    if h >= 345 or h < 15:
        if brightness < 80:
            return "Dark_Red"
        elif saturation > 0.6 and brightness > 200:
            return "Pink"
        else:
            return "Red"

    # Orange: 15-45
    elif h >= 15 and h < 45:
        if brightness < 80:
            return "Dark_Orange"
        elif brightness > 180 and saturation > 0.5:
            return "Orange"
        elif saturation < 0.4:
            return "Tan"
        else:
            return "Orange"

    # Yellow/Gold: 45-70
    elif h >= 45 and h < 70:
        if saturation > 0.6:
            if brightness > 150:
                return "Yellow"
            else:
                return "Gold"
        else:
            return "Beige"

    # Yellow-Green: 70-90
    elif h >= 70 and h < 90:
        return "Yellow_Green"

    # Green: 90-150
    elif h >= 90 and h < 150:
        if brightness < 80:
            return "Dark_Green"
        else:
            return "Green"

    # Cyan/Teal: 150-200
    elif h >= 150 and h < 200:
        if h < 175:
            return "Teal"
        else:
            return "Cyan"

    # Blue: 200-260
    elif h >= 200 and h < 260:
        if brightness < 80:
            return "Dark_Blue"
        else:
            return "Blue"

    # Purple: 260-290
    elif h >= 260 and h < 290:
        if brightness < 80:
            return "Dark_Purple"
        else:
            return "Purple"

    # Magenta/Pink: 290-345
    elif h >= 290 and h < 345:
        if brightness > 180:
            return "Pink"
        else:
            return "Magenta"

    # Brown (special case: low brightness, low saturation, warm hue)
    if brightness < 100 and saturation < 0.5 and h >= 20 and h < 60:
        return "Brown"

    return "Mixed"


def generate_color_name(color_category, existing_names):
    """Generate a unique color-based name."""
    base_names = COLOR_NAMES.get(color_category, ["image"])

    for _ in range(50):
        name = random.choice(base_names)
        number = random.randint(1, 999)
        new_name = f"{name}_{number}"

        if new_name not in existing_names:
            existing_names.add(new_name)
            return new_name

    return f"{color_category.lower()}_{random.randint(1000, 9999)}"


def organize_photos(source_folder, destination_folder):
    """Organize photos by color into folders and rename them."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")
    existing_names = set()

    files = [
        f for f in os.listdir(source_folder) if f.lower().endswith(image_extensions)
    ]
    total = len(files)

    print(f"Found {total} images to organize...\n")

    for idx, filename in enumerate(files, 1):
        file_path = os.path.join(source_folder, filename)

        # Get dominant color using K-means
        dominant_rgb = get_dominant_colors(file_path)

        if dominant_rgb:
            color = classify_color(dominant_rgb)

            # Create color folder
            color_folder = os.path.join(destination_folder, color)
            if not os.path.exists(color_folder):
                os.makedirs(color_folder)

            # Generate new color-based name
            file_ext = os.path.splitext(filename)[1]
            new_name = generate_color_name(color, existing_names)
            new_filename = f"{new_name}{file_ext}"

            # Copy with new name
            destination_path = os.path.join(color_folder, new_filename)
            shutil.copy2(file_path, destination_path)

            print(f"[{idx}/{total}] {filename} → {color}/{new_filename}")


if __name__ == "__main__":
    source = "/home/novo/Pictures/input"
    destination = "/home/novo/Pictures/organized_by_color"

    print("Starting photo organization by color with pywal-style extraction...\n")
    organize_photos(source, destination)
    print("\nDone! Photos have been organized by color and renamed.")
