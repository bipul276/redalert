"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { fetchWatchlists, addWatchlist, deleteWatchlist, WatchlistItem } from "@/lib/api_watchlist";

export default function AlertsPage() {
    const [items, setItems] = useState<WatchlistItem[]>([]);
    const [newValue, setNewValue] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadItems();
    }, []);

    async function loadItems() {
        const data = await fetchWatchlists();
        setItems(data);
        setLoading(false);
    }

    async function handleAdd(e: React.FormEvent) {
        e.preventDefault();
        if (!newValue.trim()) return;

        await addWatchlist("BRAND", newValue); // Defaulting to BRAND for MVP
        setNewValue("");
        loadItems();
    }

    async function handleDelete(id: number) {
        await deleteWatchlist(id);
        loadItems();
    }

    // Phase 8: WebPush Logic
    async function enableNotifications() {
        if (!("serviceWorker" in navigator)) return;

        const reg = await navigator.serviceWorker.register("/sw.js");
        const permission = await Notification.requestPermission();

        if (permission === "granted") {
            // Fetch public key
            const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";
            const res = await fetch(`${API_BASE}/notifications/vapid-public-key`);
            const { publicKey } = await res.json();

            const sub = await reg.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(publicKey)
            });

            // Send to backend
            const API_BASE2 = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";
            await fetch(`${API_BASE2}/notifications/subscribe`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    endpoint: sub.endpoint,
                    keys: sub.toJSON().keys,
                    user_id: 1
                })
            });
            alert("Notifications enabled!");
        }
    }

    function urlBase64ToUint8Array(base64String: string) {
        const padding = "=".repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding).replace(/\-/g, "+").replace(/_/g, "/");
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div className="text-center space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">My Safety Watchlist</h1>
                <p className="text-muted-foreground">Get notified if verified safety alerts affect your tracked items.</p>
                <button onClick={enableNotifications} className="text-xs bg-slate-800 text-white px-3 py-1 rounded mt-2">
                    🔔 Enable Push Notifications
                </button>
            </div>

            <div className="bg-card border rounded-lg p-6 shadow-sm">
                <h2 className="font-semibold mb-4">Track an Item</h2>
                <form onSubmit={handleAdd} className="flex gap-4">
                    <input
                        type="text"
                        value={newValue}
                        onChange={(e) => setNewValue(e.target.value)}
                        placeholder="e.g. Tesla, Cough Syrup, Baby Formula"
                        className="flex-1 px-4 py-2 border rounded-md bg-background focus:ring-2 focus:ring-accent outline-none"
                    />
                    <button type="submit" className="bg-accent text-accent-foreground px-6 py-2 rounded-md font-medium hover:opacity-90 transition-opacity">
                        Track Item
                    </button>
                </form>
            </div>

            <div className="space-y-4">
                <h2 className="font-semibold text-lg">Active Alerts ({items.length})</h2>
                {loading ? (
                    <p className="text-muted-foreground text-sm">Loading...</p>
                ) : items.length === 0 ? (
                    <div className="text-center py-12 bg-secondary/10 rounded-xl border border-dashed border-border/50">
                        <p className="text-lg font-medium">You’re all clear for now.</p>
                        <p className="text-sm text-muted-foreground mt-1">We’ll notify you if any new recalls match your watchlist.</p>
                    </div>
                ) : (
                    <div className="grid gap-3">
                        {items.map((item) => (
                            <div key={item.id} className="flex items-center justify-between p-4 bg-card rounded-lg border hover:border-accent/50 transition-colors">
                                <div className="flex items-center gap-4">
                                    <div className="flex flex-col">
                                        <span className="font-semibold text-lg">{item.value}</span>
                                        <div className="flex items-center gap-2 mt-1">
                                            <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground bg-secondary px-2 py-0.5 rounded">{item.type}</span>
                                            <span className="text-[10px] uppercase tracking-wider text-muted-foreground">Global</span>
                                        </div>
                                    </div>
                                </div>
                                <button
                                    onClick={() => item.id && handleDelete(item.id)}
                                    className="text-sm text-muted-foreground hover:text-destructive transition-colors px-3 py-1 rounded hover:bg-destructive/10"
                                >
                                    Remove
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
