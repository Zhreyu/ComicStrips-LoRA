
# Calvin and Hobbes Comic Strip Generation - LoRA Fine-Tuning on Flux Model

This project aims to fine-tune the **Flux.1-dev** model using **LoRA (Low-Rank Adaptation)** to generate Calvin and Hobbes comic strip images. The entire process includes scraping data, annotating the dataset using a vision model, and fine-tuning the model for image generation.

---

## Project Overview

### **Model**
The base model used for fine-tuning is [Flux.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev). This model is designed to generate comic strip images, and we fine-tune it using LoRA to create unique Calvin and Hobbes comic strip scenes.

---

## Data Preparation

### 1. **Data Collection (Scraping Reddit Images)**

We began by collecting comic strip images from Reddit posts using a custom Python scraper. The script fetches and downloads images from a specified Reddit user’s posts, handling pagination and filtering based on file types like `.jpg`, `.png`, `.jpeg`, and `.gif`. This process allowed us to build a comprehensive dataset for fine-tuning the model.

### 2. **Merging Datasets (Optional)**

Once the images were downloaded, we used `merge_datasets.py` to combine datasets from multiple sources if needed. This script also removed duplicate images to ensure the dataset is clean and ready for annotation.

### 3. **Annotating Images Using LLava Model**

After preparing the dataset, we annotated the images using the **LLava:13b** vision model through **Ollama**. The `annotate_dataset.py` script generated textual descriptions of each image, focusing on the interaction between characters in the comic strips. This annotation helped the model understand the content of the images for training.

### Annotation Example:
- Input Image: Calvin and Hobbes fishing.
- Annotated Description: *Calvin and Hobbes attempt to catch a fish while boating together.*

The annotated dataset was saved in a CSV file (`image_descriptions.csv`) for further processing.

---

## Dataset Preparation for Fine-tuning

### 4. **Text Preparation**

We ran `txt_prep.py` to convert the annotated dataset into the required format. This script generated individual text files for each image, providing detailed descriptions needed for fine-tuning the **Flux.1-dev** model.

---

## Fine-tuning the Flux Model with LoRA

### 5. **Environment Setup**

To fine-tune the model, the **AI Toolkit** repository (with submodules) is already included in this repository, so there's no need to clone it again.

To set up your environment:

```bash
cd your-repo
python -m venv venv
source venv/bin/activate
pip install torch
pip install -r requirements.txt
pip install --upgrade accelerate transformers diffusers huggingface_hub
```

### 6. **Upload Your Dataset**

Create a new folder in the root of your repository called `dataset`. Move the `.jpg`, `.jpeg`, `.png` images and their corresponding `.txt` files generated in the previous steps into this folder.

### 7. **Login to Hugging Face**

Login to Hugging Face and request access to the **Flux.1-dev** model:

1. Get a **READ** token from [Hugging Face](https://huggingface.co/).
2. Request access to [Flux.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev).
3. Run the following command and paste your access token:

```bash
huggingface-cli login
```

### 8. **Start Training**

You need to edit a configuration file for fine-tuning:

1. Copy an example config file from `config/examples/` to the `config/` folder and rename it (e.g., `calvin_and_hobbes_finetune.yml`).
2. Edit the config file:
    - Set `folder_path: "/path/to/your/dataset/folder"` to your actual dataset folder path.
3. Start the fine-tuning process:

```bash
python run.py config/calvin_and_hobbes_finetune.yml
```

The training will begin, and the model will fine-tune on your custom dataset.

---

## Model and Dataset

### **Model on Hugging Face**

The trained model is available on [Hugging Face](https://huggingface.co/your-username/ComicStrips_LoRA_FluxModel). You can download and use the fine-tuned model directly from there.

### **Dataset**

The dataset used for this project will be made available soon.

---

## Acknowledgements

Special thanks to the creators of the **AI Toolkit** for providing the tools necessary to fine-tune the Flux.1-dev model using LoRA. Their contributions have been instrumental in the success of this project.
