# Text2Img Project 🎨

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-orange.svg)

</div>

This project implements a text-to-image generation system using Stable Diffusion with CLIP score evaluation. The system can generate high-quality images from text descriptions and evaluate how well the generated images match the input prompts.

## 📁 Project Structure

```
Text2Img/
├── .git/               # Git repository files
├── output/             # Directory for storing generated images
├── run_sd.py          # Python script version of the implementation
├── run_sd.ipynb       # Jupyter notebook implementation
└── requirements.txt    # Project dependencies
```

## ✨ Features

- 🖼️ Text to image generation using Stable Diffusion
- 📊 CLIP score evaluation for image-text similarity
- 🚀 Support for mixed precision inference using Accelerate
- 💾 Automatic image saving with timestamp and CLIP score
- 🧠 Memory efficient processing with xformers support
- 📓 Jupyter notebook interface for interactive use

## 🤖 Model Information

- **Base Model**: `nguyenthb29/dat301` (Trained on Flickr8r dataset)
- **Image Resolution**: 512x512 pixels
- **CLIP Model**: ViT-B/32 for similarity scoring

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- CUDA-capable GPU (recommended)

### Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Text2Img
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Additional requirements:**
```bash
pip install git+https://github.com/openai/CLIP.git
pip install accelerate
```

## 🚀 Usage

### 📓 Using Jupyter Notebook (run_sd.ipynb)

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `run_sd.ipynb`
3. Run the cells sequentially

### 💻 Using Python Script (run_sd.py)

```bash
python run_sd.py
```

## ⚙️ Parameters

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `NUM_INFERENCE_STEPS` | 50 | Number of denoising steps |
| `GUIDANCE_SCALE` | 0.25 | Controls how much the image generation follows the prompt |
| `HEIGHT` | 512 | Output image height in pixels |
| `WIDTH` | 512 | Output image width in pixels |

## 📤 Output

Generated images are automatically saved in the `output/` directory. Each filename contains:
- 📅 Timestamp
- 📝 Prompt text (truncated)
- 📊 CLIP score

### Example filename:
<div align="center">

**Prompt**: "A fantasy-style girl with glow"  

![Sample Generated Image](output/20250608_215900_A%20fantasy-style%20girl%20with%20glow_25.44.png)

</div>

## 📊 CLIP Score Interpretation

The CLIP score indicates how well the generated image matches the input text:

| Score Range | Interpretation |
|-------------|---------------|
| > 80 | 🌟 Very high similarity |
| 60-80 | ✨ Good similarity |
| 40-60 | ⭐ Moderate similarity |
| < 40 | 💫 Low similarity |




