import React from "react";

const App: React.FC = () => {
  return (
    <div style={{ padding: "1rem", fontFamily: "system-ui" }}>
      <h1>Module: Website</h1>
      <p>Frontend van de module Website van casuse-hp.</p>
      <p>Backend hoort te draaien op <code>http://localhost:20050</code> (GET /healthz).</p>
    </div>
  );
};

export default App;
