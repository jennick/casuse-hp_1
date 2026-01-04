import React from "react";

const Dashboard: React.FC<{ modules: any[] }> = ({ modules }) => {
  /**
   * CORE = launcher
   * Modules beslissen ZELF over login / redirect
   * GEEN token checks hier (cross-origin!)
   */
  const openModule = (baseUrl: string) => {
    window.location.href = baseUrl;
  };

  return (
    <div className="dashboard">
      <h2>Modules</h2>

      <div className="tiles">
        {modules.map((m) => (
          <div
            key={m.key}
            className={`tile ${m.status === "online" ? "online" : ""}`}
          >
            <h3>{m.name}</h3>
            <p>{m.url}</p>

            <button onClick={() => openModule(m.url)}>
              Open
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
