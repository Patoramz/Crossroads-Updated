from transformers import AutoTokenizer, AutoModel
import torch

# Load the tokenizer and model for GTE-Small
tokenizer = AutoTokenizer.from_pretrained("Supabase/gte-small")
model = AutoModel.from_pretrained("Supabase/gte-small")


# Function to generate embeddings
def generate_embedding(text):
    # Encode the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Pass the encoded text to the model and get the last hidden states
    with torch.no_grad():  # This tells PyTorch not to keep track of gradients
        outputs = model(**inputs)

    # Perform mean pooling on the output tensor to get a single vector
    embeddings = outputs.last_hidden_state.mean(1)

    # Convert the tensor directly to a list for easier handling in Python
    return embeddings.squeeze().tolist()  # Use squeeze() to remove any unnecessary dimensions
