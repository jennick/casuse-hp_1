import React from "react";
import PageHeader from "../components/PageHeader";

const DashboardPage: React.FC = () => {
  return (
    <div className="card">
      <PageHeader
        title="Overzicht"
        description="Dit is het startscherm van de verkoopmodule. De belangrijkste functionaliteit op dit moment is het beheer van verkopers."
      />
      {/* Hier kun je later KPI-tegels, grafieken, etc. toevoegen */}
    </div>
  );
};

export default DashboardPage;
