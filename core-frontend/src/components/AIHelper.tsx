import React, { useState } from "react";
import { askAI } from "../api";

const AIHelper: React.FC = () => {
  const [q, setQ] = useState("");
  const [a, setA] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const ask = async () => {
    setLoading(true);
    try {
      setA(await askAI(q));
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="ai-helper">
      <h2>AI-helper</h2>
      <textarea value={q} onChange={(e) => setQ(e.target.value)} />
      <button onClick={ask} disabled={loading}>{loading ? "..." : "Vraag"}</button>
      {a && (
        <div className="ai-answer">
          <h3>{a.title}</h3>
          {a.steps && <ul>{a.steps.map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>}
          {a.code_example && <pre>{a.code_example}</pre>}
        </div>
      )}
    </div>
  );
};

export default AIHelper;
