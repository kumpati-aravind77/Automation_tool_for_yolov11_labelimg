# Automation_tool_for_yolov11_labelimg
# 🚀 TiHAN Auto Labeling & Annotation Tool

A simple and powerful GUI tool to automatically generate labels for images using **YOLOv11** and manually annotate them using **LabelImg**.

---
## Example Image

Here is an example of how the tool looks:

![Tool Image](images/your-image.png)


## 📜 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## 📖 About the Project

This GUI application is designed for preparing datasets for object detection tasks.  
It automates the labeling process using **YOLOv11** models and allows manual corrections using **LabelImg**, streamlining the dataset creation workflow.

---

## ✨ Features

- 📂 Select image folders easily.
- 🤖 Auto-generate labels using YOLOv11.
- 🧾 Automatically copy and manage your `classes.txt` file.
- 🖍️ Open LabelImg for manual annotation corrections.
- 💬 View real-time terminal logs inside the GUI.
- 🧹 Organize label files cleanly into the dataset.

---

## ⚙️ Installation

Follow these steps to install and run the tool:

```bash
# 1. Clone the repository
git clone https://github.com/your-repo-name.git
cd your-repo-name

# 2. Install required packages
pip install -r requirements.txt

# 3. Install YOLOv11 and LabelImg if not already installed
pip install ultralytics labelImg pillow
```

## 🖥️ Usage
To start the application:
```bash
python main.py
```


## 🛠️ Configuration
Update the config.py file according to your system setup:
```bash
LOGO_PATH = "assets/logo.png"  # Path to logo image
MODEL_WEIGHTS = "weights/yolov11_best.pt"  # Path to YOLOv11 trained weights
CLASSES_FILE_PATH = "classes/classes.txt"  # Path to your classes.txt file
LABELIMG_EXEC = "labelImg"  # LabelImg execution command or full path
```
## 📁 Folder Structure

Here's the layout of the project folder:
```bash
├── main.py                 # GUI main application script
├── config.py                # Configuration file
├── assets/
│   └── logo.png             # Logo image for the GUI
├── weights/
│   └── yolov11_best.pt      # Pre-trained YOLOv11 model weights
├── classes/
│   └── classes.txt          # Class names for object detection
├── README.md                # Project documentation (this file)
└── requirements.txt         # Python dependencies
```
