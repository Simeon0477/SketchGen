import os
import gc
import torch
import base64
from io import BytesIO
from pathlib import Path
from flask import Blueprint, request, jsonify
from diffusers import StableDiffusionPipeline, AnimateDiffPipeline, MotionAdapter, DDIMScheduler
from diffusers.utils import export_to_gif
from transformers import MarianMTModel, MarianTokenizer

router = Blueprint("router", __name__)

MODELS_DIR = Path(__file__).parent.parent / "models"
SD15_PATH = MODELS_DIR / "sd15"
ANIMATE_PATH = MODELS_DIR / "animatediff_adapter"
LORA_PATH = MODELS_DIR / "lora_sketch_sd15_v2"
TRANSLATOR_PATH = MODELS_DIR / "translator_fr_en"
OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE  = torch.float16 if DEVICE == "cuda" else torch.float32
print(f"Device : {DEVICE} | dtype : {DTYPE}")

# Chargement du traducteur
print("Chargement du traducteur...")
translator_model = MarianMTModel.from_pretrained(str(TRANSLATOR_PATH), low_cpu_mem_usage=True)
translator_tokenizer = MarianTokenizer.from_pretrained(str(TRANSLATOR_PATH))
translator_model.eval()
gc.collect()
print("Traducteur prêt")

# Chargement de SD 1.5
print("Chargement de SD 1.5...")
pipe_image = StableDiffusionPipeline.from_pretrained(
    str(SD15_PATH),
    torch_dtype=DTYPE,
    low_cpu_mem_usage=True,
    use_safetensors=True,
    safety_checker=None,
    feature_extractor=None,
    requires_safety_checker=False,
)
pipe_image = pipe_image.to(DEVICE)
pipe_image.enable_attention_slicing(1)
if DEVICE == "cuda":
    pipe_image.enable_vae_slicing()
gc.collect()

# Appliquer LoRA
print("Application du LoRA...")
pipe_image.load_lora_weights(str(LORA_PATH))
pipe_image.fuse_lora()
gc.collect()
print("LoRA fusionné")

print("SD 1.5 + LoRA prêt")

# Chargement d'AnimateDiff
print("Chargement AnimateDiff...")
adapter = MotionAdapter.from_pretrained(
    str(ANIMATE_PATH),
    low_cpu_mem_usage=True,
    torch_dtype=DTYPE,
)
pipe_video = AnimateDiffPipeline(
    unet=pipe_image.unet,
    text_encoder=pipe_image.text_encoder,
    tokenizer=pipe_image.tokenizer,
    vae=pipe_image.vae,
    motion_adapter=adapter,
    scheduler=DDIMScheduler.from_config(pipe_image.scheduler.config),
)
pipe_video = pipe_video.to(DEVICE)
pipe_video.enable_attention_slicing(1)
if DEVICE == "cuda":
    pipe_video.enable_vae_slicing()
gc.collect()
print("AnimateDiff prêt")

# Fonction de traduction
def translate_fr_to_en(text: str) -> str:
    with torch.no_grad():
        inputs  = translator_tokenizer(text, return_tensors="pt", padding=True)
        outputs = translator_model.generate(**inputs)
    return translator_tokenizer.decode(outputs[0], skip_special_tokens=True)

# Fonction de libération de mémoire
def free_memory():
    gc.collect()
    if DEVICE == "cuda":
        torch.cuda.empty_cache()

# Route de génération d'image
@router.route("/generate_image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt manquant"}), 400

    prompt_en = translate_fr_to_en(prompt)
    print(f"Traduit : {prompt_en}")

    try:
        with torch.no_grad():
            image = pipe_image(
                prompt=f"{prompt_en}, hand drawn pencil sketch, grayscale",
                negative_prompt="color, realistic, photo, painting, blurry",
                num_inference_steps=30,
                guidance_scale=7.5,
            ).images[0]
    finally:
        free_memory()

    output_path = OUTPUTS_DIR / "output_image.png"
    image.save(str(output_path))

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return jsonify({
        "status"   : "success",
        "image"    : img_b64,
    })

# Fonction de génération de vidéos
@router.route("/generate_video", methods=["POST"])
def generate_video():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt manquant"}), 400

    prompt_en = translate_fr_to_en(prompt)
    print(f"Traduit : {prompt_en}")

    try:
        with torch.no_grad():
            frames = pipe_video(
                prompt=f"{prompt_en}, sketch, grayscale, white background",
                negative_prompt="color, realistic, photo, painting, blurry",
                num_frames=16,
                num_inference_steps=20,
                guidance_scale=7.5,
            ).frames[0]
    finally:
        free_memory()

    output_path = str(OUTPUTS_DIR / "output_video.gif")
    export_to_gif(frames, output_path)

    with open(output_path, "rb") as f:
        gif_b64 = base64.b64encode(f.read()).decode("utf-8")

    return jsonify({
        "status"   : "success",
        "video"    : gif_b64,
    })