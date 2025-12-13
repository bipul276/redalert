export interface Recall {
    id: number;
    title: string;
    brand?: string;
    product?: string;
    category?: string;
    region: string;
    hazard_summary?: string;
    official_action?: string;
    confidence_level: 'CONFIRMED' | 'PROBABLE' | 'WATCH';
    updated_at: string;
    created_at: string;
    url?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchRecalls(region?: string, search?: string): Promise<Recall[]> {
    const params = new URLSearchParams();
    if (region) params.append("region", region);
    if (search) params.append("q", search);

    // Next.js: Ensure this fetched on server or client as appropriate.
    // Using 'no-store' for dynamic data in MVP
    const res = await fetch(`${API_BASE}/recalls?${params.toString()}`, { cache: 'no-store' });

    if (!res.ok) {
        console.error("Failed to fetch recalls");
        return [];
    }

    return res.json();
}
