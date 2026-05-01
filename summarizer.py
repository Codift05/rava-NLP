from transformers import pipeline

class SummarizerEngine:
    def __init__(self, model_name="cahya/bert2bert-indonesian-summarization"):
        self.model_name = model_name
        self.summarizer = None

    def load_model(self):
        print(f"Loading Summarizer model ({self.model_name})...")
        try:
            # We use max_length=150, min_length=40, do_sample=False as standard for summarization
            self.summarizer = pipeline("summarization", model=self.model_name)
            print("Summarizer model loaded.")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            print("Falling back to standard english summarizer (facebook/bart-large-cnn)...")
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text):
        if self.summarizer is None:
            self.load_model()
            
        print("Summarizing text...")
        if not text or len(text.strip()) == 0:
            return "No text to summarize."
            
        # Basic chunking if text is too long (transformers limit is usually 512 or 1024 tokens)
        # For simplicity, we just pass the text and let pipeline truncate if needed
        try:
            # Check length to prevent pipeline errors on very short text
            words = text.split()
            if len(words) < 20:
                return text # Too short to summarize
                
            result = self.summarizer(text, max_length=130, min_length=30, do_sample=False, truncation=True)
            return result[0]['summary_text']
        except Exception as e:
            print(f"Error during summarization: {e}")
            return f"Error: Could not generate summary. ({e})"
