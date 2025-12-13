import { Badge } from "@/components/ui/Badge";
import Link from "next/link";
import { Recall } from "@/lib/api";

const API_BASE = "http://localhost:8000/api/v1";

async function getRecall(id: string): Promise<Recall | null> {
    const res = await fetch(`${API_BASE}/recalls/${id}`, { cache: 'no-store' });
    if (!res.ok) return null;
    return res.json();
}

export default async function RecallDetailPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    const data = await getRecall(id);

    if (!data) {
        return (
            <div className="text-center py-20">
                <h1 className="text-2xl font-bold">Recall not found</h1>
                <Link href="/" className="text-accent hover:underline mt-4 inline-block">Return Home</Link>
            </div>
        );
    }

    return (
        <div className="max-w-3xl mx-auto space-y-8">
            <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                &larr; Back to search
            </Link>

            {/* Header */}
            <div className="space-y-4">
                <div className="flex items-center gap-3">
                    <Badge variant={data.confidence_level.toLowerCase() as any}>{data.confidence_level}</Badge>
                    <span className="text-sm text-muted-foreground">{new Date(data.updated_at).toLocaleDateString()} • {data.region}</span>
                </div>
                <h1 className="text-3xl font-bold leading-tight text-foreground sm:text-4xl">
                    {data.title}
                </h1>
                <p className="text-lg text-muted-foreground font-medium">
                    Brand: <span className="text-foreground">{data.brand || "Unknown"}</span>
                </p>
            </div>

            {/* Main Content (Calm Columns) */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 border-t pt-8">

                {/* Left Column: Hazard & Action */}
                <div className="md:col-span-2 space-y-8">
                    <section>
                        <h2 className="text-xl font-semibold mb-3 text-foreground">Hazard Summary</h2>
                        <div className="prose text-foreground/80 leading-relaxed">
                            <p>{data.hazard_summary || "No detailed summary available."}</p>
                        </div>
                    </section>

                    <section className="bg-secondary/30 p-6 rounded-lg border">
                        <h2 className="text-xl font-semibold mb-3 text-foreground flex items-center gap-2">
                            <span>What should I do?</span>
                        </h2>
                        <p className="text-foreground/90 leading-relaxed">
                            {data.official_action || "Please contact the manufacturer or check official sources for remedy instructions."}
                        </p>
                    </section>
                </div>

                {/* Right Column: Metadata & Sources */}
                <div className="space-y-6">
                    <div className="rounded-lg border bg-card p-5">
                        <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider text-muted-foreground">Sources</h3>
                        {data.url ? (
                            <a
                                href={data.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block w-full text-center bg-accent text-accent-foreground py-2 rounded-md hover:opacity-90 transition-opacity"
                            >
                                View Official Source &rarr;
                            </a>
                        ) : (
                            <p className="text-sm text-muted-foreground">No direct source link available.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
