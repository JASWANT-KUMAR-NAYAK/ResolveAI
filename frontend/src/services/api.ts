import type { DeviationData } from "../types/deviation";

const API_BASE_URL = "http://127.0.0.1:8000";

function mapDeviation(data: any): DeviationData {
  let dateOfOccurrence = data.date_of_occurrence ?? "";

  if (dateOfOccurrence) {
    const parsedDate = new Date(dateOfOccurrence);

    if (!Number.isNaN(parsedDate.getTime())) {
      const year = parsedDate.getFullYear();
      const month = String(parsedDate.getMonth() + 1).padStart(2, "0");
      const day = String(parsedDate.getDate()).padStart(2, "0");

      dateOfOccurrence = `${year}-${month}-${day}`;
    }
  }

  return {
    site: data.site ?? "",
    dateOfOccurrence,
    title: data.title ?? "",
    description: data.description ?? "",
    relatedProduct: data.related_product ?? null,
    relatedMaterial: data.related_material ?? null,
    batchNumber: data.batch_number ?? null,
    processParameter: data.process_parameter ?? null,
  };
}

export async function extractDeviation(text: string): Promise<DeviationData> {
  const response = await fetch(`${API_BASE_URL}/api/extract`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error("Failed to extract deviation");
  }

  const result = await response.json();

  return mapDeviation(result.data);
}

export async function analyzeDeviation(deviation: DeviationData) {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      deviation: {
        site: deviation.site || null,
        date_of_occurrence: deviation.dateOfOccurrence || null,
        title: deviation.title || null,
        description: deviation.description || null,
        related_product: deviation.relatedProduct,
        related_material: deviation.relatedMaterial,
        batch_number: deviation.batchNumber,
        process_parameter: deviation.processParameter,
      },
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyze deviation");
  }

  return response.json();
}

export async function saveDeviation(
  deviation: DeviationData,
  impact: any,
  severity: any,
  userEdits: Partial<DeviationData>
) {
  const response = await fetch(`${API_BASE_URL}/api/save`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      deviation: {
        site: deviation.site,
        date_of_occurrence: deviation.dateOfOccurrence,
        title: deviation.title,
        description: deviation.description,
        related_product: deviation.relatedProduct,
        related_material: deviation.relatedMaterial,
        batch_number: deviation.batchNumber,
        process_parameter: deviation.processParameter,
      },
      impact,
      severity,
      user_edits: userEdits,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to save deviation");
  }

  return response.json();
}

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Failed to upload document");
  }

  return response.json();
}