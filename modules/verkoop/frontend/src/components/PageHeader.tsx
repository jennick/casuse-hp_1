import React from "react";
import { useNavigate } from "react-router-dom";

interface PageHeaderProps {
  title: string;
  description?: string;
  showBack?: boolean;
  backLabel?: string;
  backTo?: string;
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  showBack = false,
  backLabel = "Terug",
  backTo,
}) => {
  const navigate = useNavigate();

  function handleBack() {
    if (backTo) {
      navigate(backTo);
    } else {
      navigate(-1);
    }
  }

  return (
    <div style={{ marginBottom: "0.75rem" }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "0.75rem",
          marginBottom: description ? "0.25rem" : 0,
        }}
      >
        {showBack && (
          <button
            type="button"
            className="button secondary"
            onClick={handleBack}
          >
            ← {backLabel}
          </button>
        )}
        <h1 style={{ margin: 0 }}>{title}</h1>
      </div>
      {description && (
        <p
          style={{
            fontSize: "0.9rem",
            color: "#4b5563",
            marginTop: 0,
          }}
        >
          {description}
        </p>
      )}
    </div>
  );
};

export default PageHeader;
