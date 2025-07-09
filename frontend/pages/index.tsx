import { useState, useEffect } from 'react';

export default function Home() {
  const [message, setMessage] = useState<string>('Loading...');

  useEffect(() => {
    // ↓↓↓ この行を修正 ↓↓↓
    fetch('http://localhost:8000/') 
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => {
        console.error(err); // コンソールにエラー詳細を出力
        setMessage('Failed to fetch from backend.');
      });
  }, []);

  return (
    <div>
      <h1>Frontend (Next.js + TypeScript)</h1>
      <p>Message from Backend: <strong>{message}</strong></p>
    </div>
  );
}