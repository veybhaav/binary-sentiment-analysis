import React, { useState } from 'react';
import './styles.css';

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Prediction failed:', error);
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
          <strong>Score:</strong> {result.score.toFixed(4)}
        </div>
      )}
    </div>
  );
}

export default App;