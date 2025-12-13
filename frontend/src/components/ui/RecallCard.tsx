import React from 'react';
import Link from 'next/link';
import { Badge } from './Badge';

interface RecallItem {
    id: string;
    title: string;
    brand: string;
    date: string;
    status: 'confirmed' | 'probable' | 'watch';
    signal_type?: string;
    hazard: string;
}

interface RecallCardProps {
    item: RecallItem;
    isTracked?: boolean;
}

export function RecallCard({ item, isTracked }: RecallCardProps) {
    const borderColors = {
        confirmed: "border-l-red-500",
        probable: "border-l-amber-500",
        watch: "border-l-slate-400"
    };

    const statusLabels = {
        confirmed: "CONFIRMED · Action Required",
        probable: "PROBABLE · Monitoring",
        watch: "WATCH · Awaiting Verification"
    };

    // Simple keyword matching for Impact Tag (Frontend categorization)
    // Only used if backend signal_type is missing
    const getImpactTag = (text: string) => {
        const lower = text.toLowerCase();
        if (lower.includes("drug") || lower.includes("pill") || lower.includes("medicine") || lower.includes("syrup") || lower.includes("tablet") || lower.includes("insulin") || lower.includes("health") || lower.includes("supplement")) return "MEDICAL";
        if (lower.includes("car") || lower.includes("brake") || lower.includes("airbag") || lower.includes("vehicle") || lower.includes("motor") || lower.includes("steering")) return "VEHICLE";
        if (lower.includes("food") || lower.includes("eat") || lower.includes("contamination") || lower.includes("allergy") || lower.includes("spice") || lower.includes("powder") || lower.includes("chilli") || lower.includes("soup") || lower.includes("chocolate") || lower.includes("salmonella") || lower.includes("listeria")) return "FOOD";
        return "PRODUCT";
    };

    // Use Backend Signal Type OR Fallback to Frontend Impact Tag
    const tagLabel = item.signal_type || getImpactTag(item.title + " " + item.hazard);

    // Normalize logic for styling keys (Uppercased or direct match)
    // Backend sends "Sample Failure" -> mapped to styling
    const tagColors: Record<string, string> = {
        "MEDICAL": "text-rose-400/90",
        "VEHICLE": "text-blue-400",
        "FOOD": "text-orange-400",
        "PRODUCT": "text-slate-500",
        // New Signals
        "Sample Failure": "text-amber-500",
        "Regulatory Action": "text-red-500",
        "Investigation": "text-slate-400",
        "International Alert": "text-indigo-400"
    };

    const tagTooltips: Record<string, string> = {
        "MEDICAL": "Potential patient safety impact",
        "VEHICLE": "Potential safety risk for drivers/passengers",
        "FOOD": "Potential contamination or labeling risk",
        "PRODUCT": "General consumer safety alert",
        // New Signals
        "Sample Failure": "Product failed lab safety tests",
        "Regulatory Action": "Official enforcement action taken",
        "Investigation": "Undergoing safety probe",
        "International Alert": "Flagged by global health agency"
    };

    // Fallback for styling lookup
    const styleKey = tagColors[tagLabel] ? tagLabel : (['MEDICAL', 'VEHICLE', 'FOOD'].includes(tagLabel) ? tagLabel : 'PRODUCT');

    return (
        <div className={`group relative flex flex-col justify-between rounded-lg border bg-card p-5 shadow-sm transition-all hover:shadow-lg hover:-translate-y-1 ${borderColors[item.status] || "border-l-slate-400"} border-l-4`}>
            {/* Tracked Label Overlay */}
            {isTracked && (
                <div className="absolute top-2 right-2 flex items-center gap-1 bg-accent/10 px-2 py-0.5 rounded-full">
                    <span className="h-1.5 w-1.5 rounded-full bg-accent animate-pulse"></span>
                    <span className="text-[9px] font-bold text-accent uppercase tracking-wider">Tracked</span>
                </div>
            )}

            {/* 1. Header: Badge */}
            <div className="mb-3 flex items-center justify-between">
                <Badge variant={item.status}>{statusLabels[item.status] || item.status.toUpperCase()}</Badge>
            </div>

            {/* 2. Body: Title (Truncated) */}
            <div className="mb-4">
                <h3 className="text-lg font-bold leading-tight line-clamp-2 group-hover:text-accent transition-colors" title={item.title}>
                    {item.title}
                </h3>
            </div>

            {/* 3. Metrics & Footer */}
            <div className="mt-auto space-y-4">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground/80">
                    <div className="group/tooltip relative">
                        <span
                            className={`cursor-help ${tagColors[tagLabel] || "text-slate-500"}`}
                            tabIndex={0} // Accessibility: allow focus
                        >
                            {tagLabel}
                        </span>
                        {/* Custom Tooltip */}
                        <div className="absolute bottom-full left-0 mb-1 w-max max-w-[200px] origin-bottom-left scale-95 opacity-0 rounded-md bg-popover px-2.5 py-1.5 text-[10px] text-popover-foreground shadow-lg shadow-black/5 transition-all duration-200 ease-out group-hover/tooltip:scale-100 group-hover/tooltip:opacity-100 group-hover/tooltip:translate-y-0 translate-y-1 border pointer-events-none z-50 font-medium tracking-normal normal-case">
                            {tagTooltips[tagLabel] || "Safety Alert"}
                        </div>
                    </div>
                    <span>·</span>
                    <span>{item.date}</span>
                </div>

                {/* Summary Excerpt */}
                <p className="text-sm leading-relaxed text-foreground/70 line-clamp-2">
                    {item.hazard}
                </p>

                <Link href={`/recall/${item.id}`} className="inline-flex items-center text-sm font-bold text-accent hover:text-accent/80 hover:underline decoration-2 underline-offset-4 transition-all focus:outline-none focus:ring-2 focus:ring-accent/50 rounded-sm">
                    Read details &rarr;
                </Link>
            </div>
        </div>
    );
}
