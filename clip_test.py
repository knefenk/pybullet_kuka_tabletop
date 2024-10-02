from transformers import AutoProcessor, AutoModelForZeroShotImageClassification
from PIL import Image
import torch
import requests

# Load model and processor
processor = AutoProcessor.from_pretrained("zer0int/CLIP-GmP-ViT-L-14")
model = AutoModelForZeroShotImageClassification.from_pretrained("zer0int/CLIP-GmP-ViT-L-14")

# Load your image
image_url = "https://www.pexels.com/photo/close-up-photo-of-white-teacup-1566308/"
image = Image.open(requests.get(image_url, stream=True).raw)

# Define your question
question = "Where do you think is the best point of contact?"

# Define potential answers
potential_answers = [
    "The center of the object",
    "The edge of the object",
    "The top of the object",
    "The bottom of the object",
    "A protruding part of the object",
    "A flat surface on the object"
]

# Combine question with potential answers
texts = [f"{question} {answer}" for answer in potential_answers]

# Process inputs
inputs = processor(images=image, text=texts, return_tensors="pt", padding=True)

# Perform inference
with torch.no_grad():
    outputs = model(**inputs)

# Get the scores
logits = outputs.logits_per_image[0]
probs = logits.softmax(dim=-1)

# Print results
print(f"Question: {question}\n")
for answer, prob in zip(potential_answers, probs):
    print(f"{answer}: {prob.item():.4f}")

# Get the best answer
best_answer = potential_answers[probs.argmax().item()]
print(f"\nBest point of contact: {best_answer}")
