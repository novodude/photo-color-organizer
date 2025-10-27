# Photo Organizer

Automatically organize and rename your image collection based on their **dominant colors**.  
Each image is analyzed to detect its main color, then copied into a matching color folder and renamed using names based on the color (e.g., `ruby_231.jpg`, `mint_88.png`, etc).

---

## Features

- Detects the **dominant color** of each image using RGB pixel analysis.
    
- Categorizes images into 25+ color families (e.g., `Red`, `Teal`, `Beige`, `Dark_Blue`, etc).
    
- Generates **unique**, names for each image based on color palettes.
    
- Automatically creates color folders and copies renamed files into them.
    
- Works with common image formats (`.jpg`, `.png`, `.webp`, `.gif`, `.tiff`, etc).
    

---

## How It Works

1. **Analyze the image**  
    The script resizes each image (150×150) and counts RGB pixel frequencies to find the dominant color.
    
2. **Classify the color**  
    Using brightness, saturation, and hue logic, each RGB value is mapped to one of the defined color categories.
    
3. **Rename and organize**  
    The file is renamed using a randomly chosen word from that color’s palette and moved into its respective folder.
    

---

## Output Structure

```
organized_by_color/
│
├── Red/
│   ├── ruby_231.jpg
│   └── scarlet_932.png
│
├── Blue/
│   ├── cobalt_413.jpg
│   └── sapphire_22.webp
│
├── Green/
│   ├── mint_582.png
│   └── forest_301.jpeg
│
└── Mixed/
    ├── prism_449.jpg
    └── rainbow_990.png
```

---

## Installation

### 1. Clone or copy the script

```
git clone https://github.com/novodude/photo-color-organizer
git cd photo-color-organizer
```

### 2. Install dependencies

```
pip install pillow
pip install numpy
pip insttall scikit-learn
```

---

## Usage

1. Edit the bottom section of the script to set your own paths:
    

```
source = "/home/novo/Pictures/input" destination = "/home/novo/Pictures/organized_by_color"
```

2. Run the script:
    

`python organize_by_color.py`

3. Sit back — your photos will be analyzed, renamed, and neatly organized!
    

---

## Supported Image Formats

- `.jpg`, `.jpeg`
    
- `.png`
    
- `.bmp`
    
- `.gif`
    
- `.tiff`
    
- `.webp`
    
---
##  License

This project is released under the **MIT License** — feel free to modify and use it for personal or commercial purposes.

🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆
🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆
🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆
