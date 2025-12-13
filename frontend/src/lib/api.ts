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
    signal_type?: string;
    updated_at: string;
    created_at: string;
    published_date?: string;
    url?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchRecalls(
    region?: string,
    search?: string,
    startDate?: string,
    endDate?: string,
    status: string[] = [],
    signalType: string[] = []
): Promise<Recall[]> {
    const params = new URLSearchParams();
    if (region) params.append("region", region);
    if (search) params.append("q", search);
    if (startDate) params.append("start_date", startDate);
    if (endDate) params.append("end_date", endDate);

    status.forEach(s => params.append("status", s.toUpperCase()));
    signalType.forEach(s => params.append("signal_type", s));

    // Next.js: Ensure this fetched on server or client as appropriate.
    // Using 'no-store' for dynamic data in MVP
    const res = await fetch(`${API_BASE}/recalls?${params.toString()}`, { cache: 'no-store' });

    if (!res.ok) {
        console.error("Failed to fetch recalls");
        return [];
    }

    return res.json();
}
