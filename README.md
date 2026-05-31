# SketchGen

SketchGen est une application web de génération d'images et de vidéos en style sketch (croquis main levée, niveaux de gris). Elle repose sur Stable Diffusion 1.5 fine-tuné via LoRA et AnimateDiff pour l'animation.

L'utilisateur saisit un prompt en français, qui est automatiquement traduit en anglais avant d'être transmis au modèle de génération.

## Structure du projet

```
SketchGen/
├── frontend/
│   └── src/
│       └── components/
│           └── Generator.tsx
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── download_models.py
│   ├── notebooks/
│   │   └── finetuning_model_image.ipynb
│   ├── models/
│   │   ├── sd15/
│   │   ├── animatediff_adapter/
│   │   ├── translator_fr_en/
│   │   └── lora_sketch/
│   ├── outputs/
│   ├── requirements.txt
│   └── run.py
```

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Simeon0477/sketchgen.git
cd sketchgen
```

### 2. Backend

Créer et activer un environnement virtuel :

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Contenu de `requirements.txt` :

```
flask
diffusers==0.30.0
transformers==4.44.0
huggingface_hub==0.24.0
accelerate==0.33.0
peft==0.12.0
torch
torchvision
sentencepiece
tqdm
```

Télécharger les modèles :

```bash
python app/download_models.py
```

Copier les poids LoRA dans le dossier attendu :

```
backend/models/lora_sketch_sd15_v2/
```

### 3. Frontend

```bash
cd frontend
npm install
```

## Lancement

### Backend

```bash
cd backend
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS
python run.py
```

Le serveur démarre sur `http://localhost:5000`.

### Frontend

```bash
cd frontend
npm run dev
```

L'interface est accessible sur `http://localhost:5173`.

## API

### POST /generate_image

```json
{ "prompt": "un chat assis sur une chaise" }
```

Réponse :

```json
{
  "status": "success",
  "image": "<base64>"
}
```

### POST /generate_video

```json
{ "prompt": "un chien qui court"}
```

Réponse :

```json
{
  "status": "success",
  "video": "<base64>"
}
```
