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

// Use the variable name exactly as it appears in your Vercel dashboard
const API_BASE = 
  process.env.NEXT_PUBLIC_API_URL || 
  "http://127.0.0.1:8000";

export async function uploadFile(file: File): Promise<IngestionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/api/ingest/csv`, {
      method: "POST",
      body: formData,
      // NOTE: Do not set 'Content-Type' manually for FormData. 
      // The browser needs to set the boundary automatically.
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Upload failed (${res.status}): ${errorText}`);
    }

    return await res.json();
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
}