import torch
import json
import random
import numpy as np
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_scheduler
from torch.optim import AdamW
import argparse
import os

class SentimentDataset(Dataset):
    def __init__(self, data_path, tokenizer):
        self.samples = []
        label_map = {"positive": 1, "negative": 0}
        with open(data_path, 'r') as f:
            for line in f:
                item = json.loads(line)
                self.samples.append({
                    'text': item['text'],
                    'label': label_map[item['label']]
                })
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        encoding = self.tokenizer(item['text'], truncation=True, padding='max_length', max_length=128, return_tensors="pt")
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(item['label'])
        }

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-data', required=True)
    parser.add_argument('-epochs', type=int, default=3)
    parser.add_argument('-lr', type=float, default=3e-5)
    args = parser.parse_args()

    set_seed(42)
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dataset = SentimentDataset(args.data, tokenizer)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    optimizer = AdamW(model.parameters(), lr=args.lr)
    num_training_steps = args.epochs * len(dataloader)
    lr_scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)

    model.train()
    for epoch in range(args.epochs):
        for batch in dataloader:
            outputs = model(
                input_ids=batch['input_ids'],
                attention_mask=batch['attention_mask'],
                labels=batch['labels']
            )
            loss = outputs.loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
    os.makedirs("model", exist_ok=True)
    model.save_pretrained("model")
    tokenizer.save_pretrained("model")

if __name__ == '__main__':
    main()