from huggingface_hub import hf_hub_download
from pathlib import Path
import os

# Désactiver XET via toutes les variables connues
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1" 
os.environ["HF_HUB_DISABLE_XET"] = "1" 
os.environ["HUGGINGFACE_HUB_VERBOSITY"] = "warning" 
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" 
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

#Chemin vers le dossier models
MODELS_DIR = Path(__file__).parent.parent / "models"

# Fichiers à télécharger pour Stable Diffusion 1.5
SD15_FILES = [
    "model_index.json",
    "scheduler/scheduler_config.json",
    "text_encoder/config.json",
    "text_encoder/model.safetensors",
    "tokenizer/merges.txt",
    "tokenizer/special_tokens_map.json",
    "tokenizer/tokenizer_config.json",
    "tokenizer/vocab.json",
    "unet/config.json",
    "unet/diffusion_pytorch_model.safetensors",
    "vae/config.json",
    "vae/diffusion_pytorch_model.safetensors",
]

# Fonction de téléchargement de Stable Diffusion 1.5
def download_sd15():
    dst_dir = MODELS_DIR / "sd15"
    if dst_dir.exists() and any(dst_dir.iterdir()):
        print("SD 1.5 déjà téléchargé")
        return
    print("Téléchargement SD 1.5...")
    for filename in SD15_FILES:
        dest = dst_dir / filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f" - {filename} déjà présent")
            continue
        print(f" - Téléchargement de : {filename}...")
        hf_hub_download(
            repo_id="runwayml/stable-diffusion-v1-5",
            filename=filename,
            local_dir=str(dst_dir)
        )
    print(f"SD 1.5 prêt — {dst_dir}")

# Fichiers à télécharger pour AnimateDiff
ANIMATEDIFF_FILES = [
    "config.json",
    "diffusion_pytorch_model.safetensors"
]

# Fonction de téléchargement d'AnimateDiff
def download_animatediff():
    dst = MODELS_DIR / "animatediff_adapter"
    if dst.exists() and any(dst.iterdir()):
        print("AnimateDiff déjà téléchargé")
        return
    print("Téléchargement AnimateDiff...")
    for filename in ANIMATEDIFF_FILES:
        dest = dst / filename
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            continue
        print(f" - Téléchargement de : {filename}...")
        hf_hub_download(
            repo_id="guoyww/animatediff-motion-adapter-v1-5-2",
            filename=filename,
            local_dir=str(dst)
        )
    print(f"AnimateDiff prêt — {dst}")

# Fonction de téléchargement du traducteur
def download_translator():
    dst = MODELS_DIR / "translator_fr_en"
    if dst.exists() and any(dst.iterdir()):
        print("Traducteur déjà téléchargé")
        return
    print("Téléchargement traducteur...")
    hf_hub_download(
        repo_id="Helsinki-NLP/opus-mt-fr-en",
        filename="config.json", local_dir=str(dst))
    hf_hub_download(
        repo_id="Helsinki-NLP/opus-mt-fr-en",
        filename="pytorch_model.bin", local_dir=str(dst))
    hf_hub_download(
        repo_id="Helsinki-NLP/opus-mt-fr-en",
        filename="tokenizer_config.json", local_dir=str(dst))
    hf_hub_download(
        repo_id="Helsinki-NLP/opus-mt-fr-en",
        filename="source.spm", local_dir=str(dst))
    hf_hub_download(
        repo_id="Helsinki-NLP/opus-mt-fr-en",
        filename="target.spm", local_dir=str(dst))
    hf_hub_download(
        repo_id="Helsinki-NLP/opus-mt-fr-en",
        filename="vocab.json", local_dir=str(dst))
    print(f"Traducteur prêt — {dst}")

# Lancement
if __name__ == "__main__":
    download_sd15()
    download_animatediff()
    download_translator()
    print("\nTous les modèles sont prêts")