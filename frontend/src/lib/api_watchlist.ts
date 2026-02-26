import { API_BASE } from "./api";

export interface WatchlistItem {
    id?: number;
    user_id?: number;
    type: string;
    value: string;
}

export async function fetchWatchlists(): Promise<WatchlistItem[]> {
    try {
        const res = await fetch(`${API_BASE}/watchlists`, { cache: 'no-store' });
        if (!res.ok) return [];
        return res.json();
    } catch (error) {
        console.error(`Error fetching watchlists from ${API_BASE}:`, error);
        return [];
    }
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
