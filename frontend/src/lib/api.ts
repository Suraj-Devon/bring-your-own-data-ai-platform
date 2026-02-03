export type NextStep = {
  title: string;
  description: string;
  priority: number;
  derived_from: string;
  category: string;
};

export type IngestionResponse = {
  insights: any[];
  charts: any[];
  next_steps: NextStep[];
};

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export async function uploadFile(
  file: File
): Promise<IngestionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(
    `${API_BASE}/api/ingest/csv`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!res.ok) {
    throw new Error("Upload failed");
  }

  return res.json();
}
