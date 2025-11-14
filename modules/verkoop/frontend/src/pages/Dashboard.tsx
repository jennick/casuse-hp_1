// modules/verkoop/frontend/src/pages/Dashboard.tsx

import React from "react";
import { Link } from "react-router-dom";

const Dashboard: React.FC = () => {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f3f4f6",
        padding: "24px",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          background: "#ffffff",
          borderRadius: "12px",
          boxShadow: "0 10px 30px rgba(15, 23, 42, 0.12)",
          padding: "24px 28px 32px",
          display: "flex",
          flexDirection: "column",
          gap: "24px",
        }}
      >
        {/* Header */}
        <header
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: "16px",
            borderBottom: "1px solid #e5e7eb",
            paddingBottom: "16px",
          }}
        >
          <div>
            <div
              style={{
                fontSize: "12px",
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                color: "#6b7280",
                fontWeight: 600,
                marginBottom: "4px",
              }}
            >
              Sales Manager
            </div>
            <h1
              style={{
                fontSize: "24px",
                lineHeight: 1.2,
                fontWeight: 700,
                color: "#111827",
                margin: 0,
              }}
            >
              Dashboard
            </h1>
            <p
              style={{
                marginTop: "6px",
                marginBottom: 0,
                fontSize: "14px",
                color: "#6b7280",
              }}
            >
              Overzicht van offertes, orders, verkopers en betalingen in één
              centrale module.
            </p>
          </div>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "flex-end",
              gap: "4px",
              fontSize: "12px",
              color: "#6b7280",
              textAlign: "right",
            }}
          >
            <span style={{ fontWeight: 600 }}>Verkoopmodule</span>
            <span>Ingelogd als admin</span>
          </div>
        </header>

        {/* Quick stats */}
        <section
          aria-label="Kernstatistieken"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            gap: "16px",
          }}
        >
          {[
            {
              label: "Actieve verkopers",
              value: "—",
              hint: "Wordt later gekoppeld aan core-data",
            },
            {
              label: "Open offertes",
              value: "—",
              hint: "Wordt later gekoppeld aan offerte-flow",
            },
            {
              label: "Open orders",
              value: "—",
              hint: "Wordt later gekoppeld aan productie/facturatie",
            },
            {
              label: "Betaling in afwachting",
              value: "—",
              hint: "Wordt later gekoppeld aan payment provider",
            },
          ].map((card, idx) => (
            <div
              key={idx}
              style={{
                borderRadius: "10px",
                border: "1px solid #e5e7eb",
                padding: "14px 16px",
                background:
                  "radial-gradient(circle at top left, #eff6ff, #ffffff)",
              }}
            >
              <div
                style={{
                  fontSize: "12px",
                  color: "#6b7280",
                  marginBottom: "4px",
                }}
              >
                {card.label}
              </div>
              <div
                style={{
                  fontSize: "22px",
                  fontWeight: 700,
                  color: "#111827",
                  marginBottom: "4px",
                }}
              >
                {card.value}
              </div>
              <div
                style={{
                  fontSize: "11px",
                  color: "#9ca3af",
                }}
              >
                {card.hint}
              </div>
            </div>
          ))}
        </section>

        {/* Navigatie-tegels naar de subpagina's */}
        <section
          aria-label="Navigatie"
          style={{
            marginTop: "8px",
          }}
        >
          <h2
            style={{
              fontSize: "16px",
              fontWeight: 600,
              color: "#111827",
              marginBottom: "12px",
            }}
          >
            Modules binnen de verkoop
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "16px",
            }}
          >
            {[
              {
                to: "/sellers",
                title: "Sellers",
                desc: "Beheer verkopers, regio's en maximale kortingen.",
              },
              {
                to: "/assignments",
                title: "Assignments",
                desc: "Toewijzing van klanten aan verkopers per regio.",
              },
              {
                to: "/quotes",
                title: "Quotes",
                desc: "Offertes aanmaken, opvolgen en koppelen aan orders.",
              },
              {
                to: "/orders",
                title: "Orders",
                desc: "Verkooporders, status en koppeling met productie.",
              },
              {
                to: "/payments",
                title: "Payments",
                desc: "Betalingsstatus, intenties en koppeling betalingsprovider.",
              },
              {
                to: "/settings",
                title: "Settings",
                desc: "Module-instellingen en nummerreeksen.",
              },
            ].map((item) => (
              <Link
                key={item.to}
                to={item.to}
                style={{
                  textDecoration: "none",
                }}
              >
                <div
                  style={{
                    borderRadius: "10px",
                    border: "1px solid #e5e7eb",
                    padding: "14px 16px",
                    background: "#f9fafb",
                    display: "flex",
                    flexDirection: "column",
                    gap: "6px",
                    transition:
                      "transform 0.12s ease-out, box-shadow 0.12s ease-out, background-color 0.12s ease-out",
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLDivElement).style.transform =
                      "translateY(-2px)";
                    (e.currentTarget as HTMLDivElement).style.boxShadow =
                      "0 10px 20px rgba(15,23,42,0.10)";
                    (e.currentTarget as HTMLDivElement).style.background =
                      "#fff";
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLDivElement).style.transform =
                      "translateY(0)";
                    (e.currentTarget as HTMLDivElement).style.boxShadow =
                      "none";
                    (e.currentTarget as HTMLDivElement).style.background =
                      "#f9fafb";
                  }}
                >
                  <div
                    style={{
                      fontSize: "14px",
                      fontWeight: 600,
                      color: "#111827",
                    }}
                  >
                    {item.title}
                  </div>
                  <div
                    style={{
                      fontSize: "12px",
                      color: "#6b7280",
                    }}
                  >
                    {item.desc}
                  </div>
                  <div
                    style={{
                      marginTop: "4px",
                      fontSize: "12px",
                      fontWeight: 500,
                      color: "#2563eb",
                    }}
                  >
                    Open module →
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
