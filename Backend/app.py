from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, TFAutoModelForSequenceClassification
import torch
import os
import time
import threading
import logging

MODEL_PATH = "./model"
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
USE_TF = os.environ.get("USE_TF", "False") == "True"

def load_model():
    try:
        if os.path.exists(os.path.join(MODEL_PATH, "pytorch_model.bin")) or os.path.exists(os.path.join(MODEL_PATH, "tf_model.h5")):
            logging.info("Loading model from ./model")
            if USE_TF:
                model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            else:
                model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        else:
            logging.info("Loading default pretrained model")
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    except Exception as e:
        logging.error(f"Model loading failed: {e}")
        raise

def model_watcher():
    global sentiment_pipeline
    last_mtime = None
    while True:
        if os.path.exists(os.path.join(MODEL_PATH, "pytorch_model.bin")):
            mtime = os.path.getmtime(os.path.join(MODEL_PATH, "pytorch_model.bin"))
            if last_mtime is None or mtime != last_mtime:
                sentiment_pipeline = load_model()
                last_mtime = mtime
        time.sleep(10)

sentiment_pipeline = load_model()
threading.Thread(target=model_watcher, daemon=True).start()

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input: TextInput):
    try:
        result = sentiment_pipeline(input.text)[0]
        return {"label": result["label"].lower(), "score": round(result["score"], 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))