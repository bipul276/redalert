"use client";

import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { useCallback, useState, useEffect } from "react";

const SEVERITY_TAGS = [
    { label: "Confirmed", value: "CONFIRMED", color: "bg-red-500/10 text-red-500 border-red-500/20" },
    { label: "Probable", value: "PROBABLE", color: "bg-orange-500/10 text-orange-500 border-orange-500/20" },
    { label: "Watch", value: "WATCH", color: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20" },
];

const SIGNAL_TAGS = [
    { label: "Recall", value: "Recall" },
    { label: "Regulatory Action", value: "Regulatory Action" },
    { label: "Sample Failure", value: "Sample Failure" },
    { label: "Investigation", value: "Investigation" },
];

export function FilterBar() {
    const router = useRouter();
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const [isOpen, setIsOpen] = useState(false);

    // Helpers
    const toggleParam = (key: string, value: string) => {
        const params = new URLSearchParams(searchParams.toString());
        const current = params.getAll(key);

        if (current.includes(value)) {
            params.delete(key);
            current.filter(c => c !== value).forEach(c => params.append(key, c));
        } else {
            params.append(key, value);
        }
        router.push(pathname + "?" + params.toString(), { scroll: false });
    };

    const setDate = (key: "start_date" | "end_date", value: string) => {
        const params = new URLSearchParams(searchParams.toString());
        if (value) {
            params.set(key, value);
        } else {
            params.delete(key);
        }
        router.push(pathname + "?" + params.toString(), { scroll: false });
    };

    const setRegion = (region: string | null) => {
        const params = new URLSearchParams(searchParams.toString());
        if (region) {
            params.set("region", region);
        } else {
            params.delete("region");
        }
        router.push(pathname + "?" + params.toString(), { scroll: false });
    }

    const applyPreset = (days: number) => {
        const end = new Date();
        const start = new Date();
        start.setDate(end.getDate() - days);

        const params = new URLSearchParams(searchParams.toString());
        params.set("end_date", end.toISOString().split('T')[0]);
        params.set("start_date", start.toISOString().split('T')[0]);
        router.push(pathname + "?" + params.toString(), { scroll: false });
    };

    const resetFilters = () => {
        const params = new URLSearchParams(searchParams.toString());
        // Keep region and query
        const region = params.get("region");
        const q = params.get("q");

        const newParams = new URLSearchParams();
        if (region) newParams.set("region", region);
        if (q) newParams.set("q", q);

        router.push(pathname + "?" + newParams.toString(), { scroll: false });
    };

    // Derived State
    const activeFiltersCount =
        (searchParams.has("start_date") ? 1 : 0) +
        (searchParams.has("end_date") ? 1 : 0) +
        searchParams.getAll("status").length +
        searchParams.getAll("signal_type").length;

    const hasActiveFilters = activeFiltersCount > 0;
    const currentRegion = searchParams.get("region");

    return (
        <div className="max-w-4xl mx-auto space-y-4">

            {/* Top Bar: Region + Toggle */}
            <div className="flex flex-wrap items-center justify-between gap-4">

                {/* Region Selector (Integrated) */}
                <div className="flex items-center bg-secondary/30 rounded-full p-1 border border-border/40">
                    <button
                        onClick={() => setRegion(null)}
                        className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${!currentRegion ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                    >
                        All Regions
                    </button>
                    <button
                        onClick={() => setRegion("US")}
                        className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${currentRegion === 'US' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                    >
                        US Only
                    </button>
                    <button
                        onClick={() => setRegion("IN")}
                        className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${currentRegion === 'IN' ? 'bg-background shadow-sm text-foreground' : 'text-muted-foreground hover:text-foreground'}`}
                    >
                        India Only
                    </button>
                </div>

                {/* Filter Toggle Button */}
                <div className="flex items-center gap-2">
                    {hasActiveFilters && !isOpen && (
                        <div className="flex gap-2">
                            {/* Summary Chips */}
                            {searchParams.has("start_date") && <span className="text-[10px] bg-accent/10 text-accent px-2 py-1 rounded-full border border-accent/20">Date Active</span>}
                            {searchParams.getAll("status").map(s => <span key={s} className="text-[10px] bg-secondary text-foreground px-2 py-1 rounded-full">{s.toLowerCase()}</span>)}
                            {searchParams.getAll("signal_type").map(s => <span key={s} className="text-[10px] bg-secondary text-foreground px-2 py-1 rounded-full">{s}</span>)}

                            <button onClick={resetFilters} className="text-[10px] px-2 py-1 text-muted-foreground hover:text-red-500">
                                Clear
                            </button>
                        </div>
                    )}

                    <button
                        onClick={() => setIsOpen(!isOpen)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${isOpen ? 'bg-secondary text-foreground' : 'bg-transparent text-muted-foreground hover:bg-secondary/50'}`}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="opacity-70">
                            <line x1="4" x2="4" y1="21" y2="14" />
                            <line x1="4" x2="4" y1="10" y2="3" />
                            <line x1="12" x2="12" y1="21" y2="12" />
                            <line x1="12" x2="12" y1="8" y2="3" />
                            <line x1="20" x2="20" y1="21" y2="16" />
                            <line x1="20" x2="20" y1="12" y2="3" />
                            <line x1="1" x2="7" y1="14" y2="14" />
                            <line x1="9" x2="15" y1="8" y2="8" />
                            <line x1="17" x2="23" y1="16" y2="16" />
                        </svg>
                        Refine alerts
                        {activeFiltersCount > 0 && !isOpen && (
                            <span className="flex items-center justify-center w-5 h-5 bg-primary text-primary-foreground text-[10px] rounded-full">
                                {activeFiltersCount}
                            </span>
                        )}
                        <span className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}>
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6" /></svg>
                        </span>
                    </button>
                </div>
            </div>

            {/* Collapsible Panel */}
            {isOpen && (
                <div className="bg-secondary/20 rounded-xl p-5 border border-border/50 space-y-5 animate-in slide-in-from-top-2 fade-in duration-200">

                    {/* Date Section */}
                    <div className="space-y-3">
                        <div className="flex items-center justify-between">
                            <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Time Range</label>
                            <div className="flex gap-2">
                                <button onClick={() => applyPreset(7)} className="text-[10px] px-2 py-1 rounded border border-border/50 hover:bg-background transition-colors">Last 7d</button>
                                <button onClick={() => applyPreset(30)} className="text-[10px] px-2 py-1 rounded border border-border/50 hover:bg-background transition-colors">Last 30d</button>
                                <button onClick={() => applyPreset(90)} className="text-[10px] px-2 py-1 rounded border border-border/50 hover:bg-background transition-colors">Last 90d</button>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <input
                                type="date"
                                className="bg-background border border-input/60 rounded-md px-3 py-1.5 text-sm w-40 focus:ring-1 focus:ring-primary outline-none"
                                value={searchParams.get("start_date") || ""}
                                onChange={(e) => setDate("start_date", e.target.value)}
                            />
                            <span className="text-muted-foreground/50">to</span>
                            <input
                                type="date"
                                className="bg-background border border-input/60 rounded-md px-3 py-1.5 text-sm w-40 focus:ring-1 focus:ring-primary outline-none"
                                value={searchParams.get("end_date") || ""}
                                onChange={(e) => setDate("end_date", e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="h-px bg-border/40"></div>

                    {/* Filter Tags: Confidence */}
                    <div className="space-y-3">
                        <label className="text-[10px] font-bold text-muted-foreground uppercase opacity-70 tracking-widest">Filter by Confidence</label>
                        <div className="flex flex-wrap gap-2">
                            {SEVERITY_TAGS.map((tag) => {
                                const isActive = searchParams.getAll("status").includes(tag.value);
                                return (
                                    <button
                                        key={tag.value}
                                        onClick={() => toggleParam("status", tag.value)}
                                        className={`
                                            text-xs font-medium px-3 py-1.5 rounded-full border transition-all
                                            ${isActive ? tag.color + " ring-1 ring-inset ring-current" : "bg-background border-border hover:border-foreground/30 text-muted-foreground hover:text-foreground"}
                                        `}
                                    >
                                        {tag.label}
                                    </button>
                                )
                            })}
                        </div>
                    </div>

                    {/* Filter Tags: Signal */}
                    <div className="space-y-3">
                        <label className="text-[10px] font-bold text-muted-foreground uppercase opacity-70 tracking-widest">Filter by Signal</label>
                        <div className="flex flex-wrap gap-2">
                            {SIGNAL_TAGS.map((tag) => {
                                const isActive = searchParams.getAll("signal_type").includes(tag.value);
                                return (
                                    <button
                                        key={tag.value}
                                        onClick={() => toggleParam("signal_type", tag.value)}
                                        className={`
                                            text-xs font-medium px-3 py-1.5 rounded-full border transition-all
                                            ${isActive ? "bg-accent/10 border-accent/30 text-accent rings-1 ring-accent/20" : "bg-background border-border hover:border-foreground/30 text-muted-foreground hover:text-foreground"}
                                        `}
                                    >
                                        {tag.label}
                                    </button>
                                )
                            })}
                        </div>
                    </div>

                    {/* Footer Actions */}
                    {hasActiveFilters && (
                        <div className="pt-2 flex justify-end border-t border-border/40">
                            <button
                                onClick={resetFilters}
                                className="text-xs text-red-400 hover:text-red-500 font-medium px-2 py-1"
                            >
                                Clear all filters
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
