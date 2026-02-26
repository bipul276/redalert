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

export const isServer = typeof window === 'undefined';

export const API_BASE = isServer
    ? (process.env.INTERNAL_API_URL || "http://127.0.0.1:8000/api/v1")
    : (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1");

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

    try {
        const res = await fetch(`${API_BASE}/recalls?${params.toString()}`, { cache: 'no-store' });

        if (!res.ok) {
            console.error(`Failed to fetch recalls from ${API_BASE}. Status: ${res.status}`);
            return [];
        }

        return res.json();
    } catch (error) {
        console.error(`Network error fetching recalls from ${API_BASE}:`, error);
        return [];
    }
}

// --- AUTHENTICATION ---
const TOKEN_KEY = "redalert_admin_token";

export function getToken(): string | null {
    if (typeof window !== "undefined") {
        return localStorage.getItem(TOKEN_KEY);
    }
    return null;
}

export function logout() {
    if (typeof window !== "undefined") {
        localStorage.removeItem(TOKEN_KEY);
        window.location.href = "/admin/login";
    }
}

export async function login(email: string, pass: string, code: string): Promise<boolean> {
    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password: pass, totp_code: code }),
        });

        if (!res.ok) return false;

        const data = await res.json();
        if (data.access_token) {
            localStorage.setItem(TOKEN_KEY, data.access_token);
            return true;
        }
        return false;
    } catch (e) {
        console.error("Login Error", e);
        return false;
    }
}

// --- ADMIN ACTIONS ---

export async function updateRecall(id: number, data: Partial<Recall>): Promise<boolean> {
    const token = getToken();
    if (!token) return false;

    const res = await fetch(`${API_BASE}/admin/${id}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });

    return res.ok;
}

export async function deleteRecall(id: number): Promise<boolean> {
    const token = getToken();
    if (!token) return false;

    const res = await fetch(`${API_BASE}/admin/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    return res.ok;
}
