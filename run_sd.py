# Import Libraries
import torch
from diffusers import DiffusionPipeline
import clip
from PIL import Image
from tqdm import tqdm 
from torchvision import transforms
import numpy as np
import os
import datetime as dt
# Param definition 
rand_seed = torch.manual_seed(42)
NUM_INFERENCE_STEPS = 50
GUIDANCE_SCALE = 0.25
HEIGHT = 512
WIDTH = 512

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Model 
model_name = "nguyenthb29/dat301" # Our trained SD on Flickr8r dataset

# Initialize pipeline and CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
pipeline = DiffusionPipeline.from_pretrained(model_name, torch_dtype = torch.float16 if device == "cuda" else torch.float32)
pipeline = pipeline.to(device)

# Load CLIP model
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

def calculate_clip_score(image, text, model, preprocess):
    """
    Calculate CLIP score between an image and text prompt
    """
    # Preprocess image and encode
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
        
        # Encode text
        text = clip.tokenize([text]).to(device)
        text_features = model.encode_text(text)
        
        # Normalize features
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        # Calculate similarity
        similarity = (100.0 * image_features @ text_features.T).item()
        
    return similarity

def text2img(prompt, pipeline):
    # Generate timestamp for unique filename
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    images = pipeline(
        prompt, 
        guidance_scale = GUIDANCE_SCALE,
        num_inference_steps = NUM_INFERENCE_STEPS,
        height = HEIGHT,
        width = WIDTH,
        generator = rand_seed
    )
    generated_image = images.images[0]
    
    # Calculate CLIP score
    clip_score = calculate_clip_score(generated_image, prompt, clip_model, clip_preprocess)
    
     # Create filename from prompt (clean it up for valid filename)
    clean_prompt = "".join(x for x in prompt[:30] if x.isalnum() or x in (' ', '-', '_')).strip()
    filename = f"{timestamp}_{clean_prompt}.png"
    
    # Save the image
    save_path = os.path.join(OUTPUT_DIR, filename)
    generated_image.save(save_path)
    print(f"Image saved to: {save_path}")
    
    return generated_image, clip_score

# Example usage with different prompts
prompts = [
    # "A futuristic cityscape at night with glowing neon lights",
    # "An ancient castle on a hill surrounded by mist",
    # "A peaceful beach during sunset with waves gently crashing on the shore",
    # "A dense forest with rays of sunlight filtering through the trees",
    # "A bustling marketplace in a medieval village",
    # "A cozy cabin in the snowy mountains",
    # "An underwater scene with colorful coral reefs and fish",
    # "A fantasy landscape with dragons flying in the sky",
    # "A serene lake surrounded by autumn trees",
    # "A futuristic space station orbiting a distant planet"
    # "A high-resolution, photorealistic image of a brown chicken standing on green grass during a sunny day, with soft shadows and detailed feather textures, blue sky with light clouds in the background, natural lighting, DSLR-style depth of field"
    # "A realistic image of a chicken standing on a grassy field under a blue sky, detailed feathers, natural lighting"
    "A fantasy-style girl with glowing eyes and flowing silver hair, wearing an elegant robe made of stars and moonlight, standing on a mountain under a starry sky, magical atmosphere, epic cinematic lighting"


    
]

# Generate images and calculate CLIP scores
for prompt in prompts:
    image, score = text2img(prompt, pipeline)
    print(f"Prompt: {prompt}")
    print(f"CLIP Score: {score:.2f}")