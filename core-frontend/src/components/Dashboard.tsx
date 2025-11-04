import React from "react";
const Dashboard: React.FC<{ modules: any[] }> = ({ modules }) => (
  <div className="dashboard">
    <h2>Modules</h2>
    <div className="tiles">
      {modules.map((m) => (
        <div key={m.key} className={`tile ${m.status === "online" ? "online" : ""}`}>
          <h3>{m.name}</h3>
          <p>{m.url}</p>
          <button onClick={() => (window.location.href = m.url)}>Open</button>
        </div>
      ))}
    </div>
  </div>
);
export default Dashboard;
