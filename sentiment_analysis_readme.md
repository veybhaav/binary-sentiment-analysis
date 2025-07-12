# ✨ Binary Sentiment Analysis Microservice

A fully containerized, end-to-end microservice for **binary sentiment analysis** using a Hugging Face Transformer model. Includes:

- Python FastAPI backend for inference
- Standalone fine-tuning script
- React frontend UI
- Docker Compose setup for local deployment

---

## 📊 Project Structure

```bash
binary-sentiment-analysis/
├── app/                       # Backend API
│   ├── app.py
│   ├── model_loader.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # React Frontend
│   ├── src/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── frontend.Dockerfile
├── model/                    # Saved fine-tuned model (ignored in Git)
├── data.jsonl                # Fine-tuning dataset
├── finetune.py               # Model fine-tuning script
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 📅 Prerequisites

- Docker Desktop (Windows/Linux/macOS)
- Python 3.8+
- Node.js & npm (if running frontend outside Docker)

---

## 🧱 Setup & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/binary-sentiment-analysis.git
cd binary-sentiment-analysis
```

### 2. Build & Run with Docker Compose

```bash
docker compose up --build
```

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:3000](http://localhost:3000)

---

## 🔍 API Documentation

### POST `/predict`

**Description**: Returns the sentiment prediction

**Request Body:**

```json
{
  "text": "I love this!"
}
```

**Response:**

```json
{
  "label": "positive",
  "score": 0.9876
}
```

---

## 🔧 Fine-Tuning

### Dataset Format: `data.jsonl`

```jsonl
{"text": "Great product!", "label": "positive"}
{"text": "Worst experience ever.", "label": "negative"}
```

### Run Fine-Tuning Script

```bash
python finetune.py --data data.jsonl --epochs 3 --lr 3e-5
```

- Saves model to `./model/`
- Automatically picked up by backend on restart

---

## 🎨 Frontend UI

**Features:**

- Text area input
- Predict button
- Shows label and score

**React Code (App.jsx):**

```jsx
import React, { useState } from 'react';
import './styles.css';

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Prediction failed:", error);
    }
  };

  return (
    <div className="container">
      <h2>Sentiment Analysis</h2>
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows={5} cols={50} />
      <br />
      <button onClick={handlePredict}>Predict</button>
      {result && (
        <div className="result">
          <strong>Label:</strong> {result.label} <br/>
          <strong>Score:</strong> {result.score}
        </div>
      )}
    </div>
  );
}

export default App;
```

Access the UI at: `http://localhost:3000`

---


## 📅 Model Notes

- Base model: `distilbert-base-uncased`
- Can be fine-tuned on any binary sentiment dataset
- Uses PyTorch by default

> ⚠️ Models over 100MB should be excluded from Git via `.gitignore`:

```gitignore
model/
*.pt
*.safetensors
```

---

## 🌟 Optional Enhancements

- Live typing inference
- GraphQL API support
- Async batch inference
- Model quantization (ONNX / bitsandbytes)
- TypeScript React frontend
- GitHub Actions CI/CD pipeline

---

## 📈 Performance

| Device   | Training Time (3 Epochs) | Inference Time |
| -------- | ------------------------ | -------------- |
| CPU      | \~2 min                  | \~200ms        |
| GPU (T4) | \~15 sec                 | \~40ms         |

---

## 🙏 Credits

Built by [Vaibhav Jaitwal](https://github.com/veybhaav) MIT License

---

## 📁 Local Development Commands (optional)

```bash
# Run backend without Docker
cd app
uvicorn app:app --reload --port 8000

# Run frontend without Docker
cd frontend
npm install
npm start
```

---

## 🚫 Troubleshooting

- **CORS Error**: Ensure `http://localhost:3000` is allowed in backend CORS middleware.
- **Large file error**: Use Git LFS or add to `.gitignore`.
- **White screen**: Check `frontend/src/index.js` is present and correctly importing `App.jsx`.

Need help? Open an [issue](https://github.com/your-username/binary-sentiment-analysis/issues).

