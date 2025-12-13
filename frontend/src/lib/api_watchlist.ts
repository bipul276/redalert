// Ideally use env var, but for MVP absolute localhost URL is safe for both client/server in this setup
// Ideally use env var, but for MVP absolute localhost URL is safe for both client/server in this setup
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface WatchlistItem {
    id?: number;
    user_id?: number;
    type: string;
    value: string;
}

export async function fetchWatchlists(): Promise<WatchlistItem[]> {
    const res = await fetch(`${API_BASE}/watchlists`, { cache: 'no-store' });
    if (!res.ok) return [];
    return res.json();
}

export async function addWatchlist(type: string, value: string): Promise<WatchlistItem | null> {
    const res = await fetch(`${API_BASE}/watchlists`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, value, user_id: 1 }) // Hardcoded user_id for MVP
    });
    if (!res.ok) return null;
    return res.json();
}

export async function deleteWatchlist(id: number): Promise<boolean> {
    const res = await fetch(`${API_BASE}/watchlists/${id}`, { method: 'DELETE' });
    return res.ok;
}
