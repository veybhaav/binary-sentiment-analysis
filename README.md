🌟 Binary Sentiment Analysis Microservice

A fully containerized, end-to-end microservice for binary sentiment analysis using a Hugging Face Transformer model. Includes:

Python FastAPI backend for inference

Standalone fine-tuning script

React frontend UI

Docker Compose setup for local deployment

🌐 Demo Screenshots

(You can optionally embed demo video or screenshots here)



📊 Project Structure

binary-sentiment-analysis/
├── app/                       # Backend API
│   ├── app.py
│   ├── model_loader.py
│   └── requirements.txt
├── frontend/                 # React Frontend
│   ├── src/
│   │   └── App.jsx
│   └── package.json
├── model/                    # Saved fine-tuned model (ignored in Git)
├── data.jsonl                # Fine-tuning dataset
├── finetune.py               # Model fine-tuning script
├── docker-compose.yml
├── Dockerfile (backend)
├── frontend.Dockerfile       # Dockerfile for React app
├── .gitignore
└── README.md

📅 Prerequisites

Docker Desktop (Windows/Linux/macOS)

Python 3.8+

Node.js & npm (if running frontend outside Docker)

🧱 Setup & Run Instructions

1. Clone the Repository

git clone https://github.com/your-username/binary-sentiment-analysis.git
cd binary-sentiment-analysis

2. Build & Run with Docker Compose

docker compose up --build

Backend: http://localhost:8000

Frontend: http://localhost:3000

🔍 API Documentation

POST /predict

Description: Returns the sentiment prediction

Request Body:

{
  "text": "I love this!"
}

Response:

{
  "label": "positive",
  "score": 0.9876
}

🔧 Fine-Tuning

Dataset Format: data.jsonl

{"text": "Great product!", "label": "positive"}
{"text": "Worst experience ever.", "label": "negative"}

Run Fine-Tuning Script

python finetune.py --data data.jsonl --epochs 3 --lr 3e-5

Saves model to ./model/

Automatically picked up by backend on restart

🎨 Frontend UI

Features:

Text area input

Predict button

Shows label and score

Access the UI at: http://localhost:3000

🚀 Deployment

Deploy Frontend to Vercel

Push your project to GitHub

Go to vercel.com > Import Project > Link GitHub repo

Set root to frontend/ and framework to React

Deploy

Deploy Backend to Render

Zip only the app/, model/, and Dockerfile

Go to render.com

Create a new Web Service from GitHub or zip

Set build command: pip install -r requirements.txt

Start command: uvicorn app:app --host 0.0.0.0 --port 8000

Choose free instance (CPU-only)

📅 Model Notes

Base model: distilbert-base-uncased

Can be fine-tuned on any binary sentiment dataset

Uses PyTorch by default

⚠️ Models over 100MB should be excluded from Git via .gitignore:

model/
*.pt
*.safetensors

🌟 Optional Enhancements

Live typing inference

GraphQL API support

Async batch inference

Model quantization (ONNX / bitsandbytes)

TypeScript React frontend

GitHub Actions CI/CD pipeline

📈 Performance

Device

Training Time (3 Epochs)

Inference Time

CPU

~2 min

~200ms

GPU (T4)

~15 sec

~40ms

🙏 Credits

Built by Vaibhav Jaitwal
MIT License

📁 Local Development Commands (optional)

# Run backend without Docker
cd app
uvicorn app:app --reload --port 8000

# Run frontend without Docker
cd frontend
npm install
npm start

🚫 Troubleshooting

CORS Error: Ensure http://localhost:3000 is allowed in backend CORS middleware.

Large file error: Use Git LFS or add to .gitignore.

White screen: Check frontend/src/index.js is present and correctly importing App.jsx.
