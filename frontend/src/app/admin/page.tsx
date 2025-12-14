"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchRecalls, Recall, updateRecall, deleteRecall, getToken, logout } from "@/lib/api";
import { Badge } from "@/components/ui/Badge";
import { LogOut } from "lucide-react";

export default function AdminPage() {
    const router = useRouter();
    const [recalls, setRecalls] = useState<Recall[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = getToken();
        if (!token) {
            router.push("/admin/login");
            return;
        }
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

    if (loading) return <div className="p-8 text-neutral-400">Verifying access...</div>;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight">Admin Dashboard</h1>
                    <p className="text-sm text-neutral-400">Secure Access • {recalls.length} Records</p>
                </div>

                <div className="flex items-center gap-4">
                    <button
                        onClick={logout}
                        className="flex items-center gap-2 text-sm text-neutral-400 hover:text-white transition-colors px-3 py-2 rounded-lg hover:bg-neutral-800"
                    >
                        <LogOut className="w-4 h-4" />
                        Logout
                    </button>
                    <Badge variant="default">{recalls.length} Recalls</Badge>
                </div>
            </div>

            <div className="rounded-md border border-neutral-800 bg-neutral-900/50 backdrop-blur-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-neutral-900 border-b border-neutral-800">
                            <tr>
                                <th className="p-4 font-medium text-neutral-400">ID</th>
                                <th className="p-4 font-medium text-neutral-400">Status</th>
                                <th className="p-4 font-medium text-neutral-400">Title</th>
                                <th className="p-4 font-medium text-neutral-400">Brand</th>
                                <th className="p-4 font-medium text-neutral-400">Region</th>
                                <th className="p-4 font-medium text-right text-neutral-400">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-neutral-800">
                            {recalls.map((recall) => (
                                <tr key={recall.id} className="hover:bg-neutral-800/30 transition-colors">
                                    <td className="p-4 font-mono text-xs text-neutral-500">{recall.id}</td>
                                    <td className="p-4">
                                        <Badge variant={recall.confidence_level.toLowerCase() as any}>
                                            {recall.confidence_level}
                                        </Badge>
                                    </td>
                                    <td className="p-4 max-w-md truncate font-medium">{recall.title}</td>
                                    <td className="p-4 text-neutral-400">{recall.brand || "-"}</td>
                                    <td className="p-4 text-neutral-400">{recall.region}</td>
                                    <td className="p-4 text-right space-x-2">
                                        {recall.confidence_level !== 'CONFIRMED' && (
                                            <button
                                                onClick={() => handleStatusChange(recall.id, 'CONFIRMED')}
                                                className="text-xs px-2 py-1 bg-green-500/10 text-green-500 rounded hover:bg-green-500/20 border border-green-500/20"
                                            >
                                                Confirm
                                            </button>
                                        )}
                                        <button
                                            onClick={() => handleDelete(recall.id)}
                                            className="text-xs px-2 py-1 bg-red-500/10 text-red-500 rounded hover:bg-red-500/20 border border-red-500/20"
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
