import React from "react";
import { useNavigate } from "react-router-dom";
import type { Lang } from "../App";

type Props = {
  lang: Lang;
};

const texts: Record<Lang, { title: string; intro: string }> = {
  en: {
    title: "Quotes",
    intro: "Here we will show created quotes and their status.",
  },
  es: {
    title: "Cotizaciones",
    intro: "Aquí mostraremos las cotizaciones creadas y su estado.",
  },
};

const QuotesPage: React.FC<Props> = ({ lang }) => {
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

export default QuotesPage;
