# tiny_llama_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class TinyLlamaChat:
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v0.1"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate_response(self, prompt, max_length=50, num_return_sequences=1):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=2,
            num_beams=2,
            early_stopping=True
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
