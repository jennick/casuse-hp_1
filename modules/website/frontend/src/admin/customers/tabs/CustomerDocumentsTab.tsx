import { useEffect, useState } from "react";
import { apiFetch } from "@/shared/api/apiClient";

type Document = {
  id: string;
  type: string;
  title: string;
  filename: string;
  created_at: string;
  download_url: string;
};

type Props = {
  customerId: string;
};

export default function CustomerDocumentsTab({ customerId }: Props) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDocuments();
  }, [customerId]);

  async function fetchDocuments() {
    try {
      const data = await apiFetch<unknown>(
        `/api/admin/customers/${customerId}/documents`
      );

      setDocuments(Array.isArray(data) ? data : []);
    } catch {
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div>Documenten laden…</div>;
  if (documents.length === 0) return <div>Geen documenten.</div>;

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Titel</th>
          <th>Bestand</th>
          <th>Aangemaakt</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {documents.map((doc) => (
          <tr key={doc.id}>
            <td>{doc.type}</td>
            <td>{doc.title}</td>
            <td>{doc.filename}</td>
            <td>{new Date(doc.created_at).toLocaleString("nl-BE")}</td>
            <td>
              <a href={doc.download_url} target="_blank" rel="noopener noreferrer">
                Download
              </a>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
