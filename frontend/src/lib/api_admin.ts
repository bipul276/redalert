import { Recall } from "./api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";
const ADMIN_SECRET = "redalert_admin_secret_123";

export async function updateRecall(id: number, data: Partial<Recall>): Promise<Recall | null> {
    const res = await fetch(`${API_BASE}/admin/${id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-Admin-Secret': ADMIN_SECRET
        },
        body: JSON.stringify(data)
    });
    if (!res.ok) return null;
    return res.json();
}

export async function deleteRecall(id: number): Promise<boolean> {
    const res = await fetch(`${API_BASE}/admin/${id}`, {
        method: 'DELETE',
        headers: {
            'X-Admin-Secret': ADMIN_SECRET
        }
    });
    return res.ok;
}
