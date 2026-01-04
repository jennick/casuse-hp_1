import React from "react";

export type TabItem = {
  key: string;
  label: string;
  content: React.ReactNode;
  disabled?: boolean;
};

export type TabsProps = {
  tabs: TabItem[];
  activeKey: string;
  onChange: (key: string) => void;
  className?: string;
};

export default function Tabs({
  tabs,
  activeKey,
  onChange,
  className,
}: TabsProps) {
  const activeTab = tabs.find((t) => t.key === activeKey);

  return (
    <div className={className}>
      {/* TAB HEADERS */}
      <div
        style={{
          display: "flex",
          borderBottom: "1px solid #ddd",
          marginBottom: "1rem",
          gap: "0.25rem",
        }}
      >
        {tabs.map((tab) => {
          const isActive = tab.key === activeKey;

          return (
            <button
              key={tab.key}
              type="button"
              disabled={tab.disabled}
              onClick={() => {
                if (!tab.disabled) onChange(tab.key);
              }}
              style={{
                padding: "0.5rem 1rem",
                border: "none",
                borderBottom: isActive
                  ? "2px solid #2563eb"
                  : "2px solid transparent",
                background: "transparent",
                cursor: tab.disabled ? "not-allowed" : "pointer",
                fontWeight: isActive ? 600 : 400,
                color: tab.disabled ? "#aaa" : "#111",
              }}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT */}
      <div>
        {activeTab ? (
          activeTab.content
        ) : (
          <div style={{ color: "#777" }}>
            Geen tab geselecteerd.
          </div>
        )}
      </div>
    </div>
  );
}
