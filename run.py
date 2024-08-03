from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Define the local directory where your model and tokenizer are saved
local_model_dir = "/app/llama-2-7b"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_model_dir)

# Load the model manually
model = AutoModelForCausalLM.from_pretrained(local_model_dir, state_dict=torch.load(f"{local_model_dir}/pytorch_model.bin"))

# Set the model to evaluation mode
model.eval()

# Check if a GPU is available and if so, use it
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define a function to generate text
def generate_text(prompt, max_length=None):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    # Generate text without a predefined maximum length
    outputs = model.generate(inputs['input_ids'], max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    max_length = data.get("max_length", 1000)  # You can set a high value for max_length or handle it as needed
    generated_text = generate_text(prompt, max_length)
    return jsonify({"generated_text": generated_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



