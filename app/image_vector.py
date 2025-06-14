import torch
import clip
import numpy as np
from PIL import Image


def init_models():
    global device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    global clip_model, preprocess_clip
    clip_model, preprocess_clip = clip.load("ViT-B/16", device=device)


def extract_image_vector(image: Image.Image) -> np.ndarray:
    clip_img = preprocess_clip(image).unsqueeze(0).to(device)

    with torch.no_grad():
        clip_emb = clip_model.encode_image(clip_img).cpu().numpy().flatten()

    clip_emb = clip_emb / np.linalg.norm(clip_emb)

    return clip_emb
