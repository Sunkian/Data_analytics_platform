from transformers import pipeline

def load_llama_model():
    return pipeline('text2sql', model="meta-llama/Meta-Llama-3-70B")
