import React from "react";
import { useNavigate } from "react-router-dom";
import type { Lang } from "../App";

type Props = {
  lang: Lang;
};

const texts: Record<Lang, { title: string; intro: string }> = {
  en: {
    title: "Sellers",
    intro: "Here you can manage sales people, regions and permissions.",
  },
  es: {
    title: "Vendedores",
    intro: "Aquí puedes gestionar vendedores, regiones y permisos.",
  },
};

const SellersPage: React.FC<Props> = ({ lang }) => {
  const t = texts[lang];
  const navigate = useNavigate();

  return (
    <section>
      <button
        type="button"
        onClick={() => navigate(-1)}
        className="mb-3 inline-flex items-center rounded-md border border-slate-300 px-3 py-1 text-xs font-medium text-slate-700 hover:bg-slate-100"
      >
        ← Back
      </button>
      <h2 className="text-2xl font-semibold mb-2">{t.title}</h2>
      <p className="text-sm text-slate-700">{t.intro}</p>
    </section>
  );
};

export default SellersPage;
