"use client";

import { useEffect, useState } from "react";
import { fetchRecalls, Recall } from "@/lib/api";
import { updateRecall, deleteRecall } from "@/lib/api_admin";
import { Badge } from "@/components/ui/Badge";

export default function AdminPage() {
    const [recalls, setRecalls] = useState<Recall[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    async function loadData() {
        // Admin sees all, no filter
        const data = await fetchRecalls();
        setRecalls(data);
        setLoading(false);
    }

    async function handleStatusChange(id: number, newStatus: 'CONFIRMED' | 'PROBABLE' | 'WATCH') {
        await updateRecall(id, { confidence_level: newStatus });
        loadData();
    }

    async function handleDelete(id: number) {
        if (!confirm("Are you sure?")) return;
        await deleteRecall(id);
        loadData();
    }

    if (loading) return <div className="p-8">Loading dashboard...</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold tracking-tight">Admin Dashboard</h1>
                <Badge variant="default">{recalls.length} Total Recalls</Badge>
            </div>

            <div className="rounded-md border bg-card">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-muted/50 border-b">
                            <tr>
                                <th className="p-4 font-medium">ID</th>
                                <th className="p-4 font-medium">Status</th>
                                <th className="p-4 font-medium">Title</th>
                                <th className="p-4 font-medium">Brand</th>
                                <th className="p-4 font-medium">Region</th>
                                <th className="p-4 font-medium text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y">
                            {recalls.map((recall) => (
                                <tr key={recall.id} className="hover:bg-muted/10">
                                    <td className="p-4 font-mono text-xs">{recall.id}</td>
                                    <td className="p-4">
                                        <Badge variant={recall.confidence_level.toLowerCase() as any}>
                                            {recall.confidence_level}
                                        </Badge>
                                    </td>
                                    <td className="p-4 max-w-md truncate">{recall.title}</td>
                                    <td className="p-4">{recall.brand || "-"}</td>
                                    <td className="p-4">{recall.region}</td>
                                    <td className="p-4 text-right space-x-2">
                                        {/* Quick Actions */}
                                        {recall.confidence_level !== 'CONFIRMED' && (
                                            <button
                                                onClick={() => handleStatusChange(recall.id, 'CONFIRMED')}
                                                className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded hover:bg-green-200"
                                            >
                                                Confirm
                                            </button>
                                        )}
                                        <button
                                            onClick={() => handleDelete(recall.id)}
                                            className="text-xs px-2 py-1 bg-red-100 text-red-800 rounded hover:bg-red-200"
                                        >
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
