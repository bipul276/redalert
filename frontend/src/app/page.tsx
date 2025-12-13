import { RecallCard } from "@/components/ui/RecallCard";
import { fetchRecalls, Recall } from "@/lib/api";
import { fetchWatchlists, WatchlistItem } from "@/lib/api_watchlist";
import { FilterBar } from "@/components/ui/FilterBar";

export default async function Home({ searchParams }: {
    searchParams: Promise<{
        q?: string;
        region?: string;
        start_date?: string;
        end_date?: string;
        status?: string | string[];
        signal_type?: string | string[];
    }>
}) {
    const params = await searchParams;
    const query = params.q;
    const region = params.region;

    // Normalize params (Next.js can return string or array)
    const status = Array.isArray(params.status) ? params.status : params.status ? [params.status] : [];
    const signalType = Array.isArray(params.signal_type) ? params.signal_type : params.signal_type ? [params.signal_type] : [];

    // Parallel fetch for recalls and watchlist
    const [recalls, watchlist] = await Promise.all([
        fetchRecalls(region, query, params.start_date, params.end_date, status, signalType),
        fetchWatchlists() // Fetch user's tracked items
    ]);

    // Separation Logic
    const trackedRecalls: Recall[] = [];
    const otherRecalls: Recall[] = [];

    if (watchlist && watchlist.length > 0) {
        recalls.forEach((recall: Recall) => {
            const isMatch = watchlist.some((w: WatchlistItem) => {
                const watchVal = w.value.toLowerCase();
                return (recall.brand && recall.brand.toLowerCase().includes(watchVal)) ||
                    (recall.title && recall.title.toLowerCase().includes(watchVal));
            });

            if (isMatch) {
                trackedRecalls.push(recall);
            } else {
                otherRecalls.push(recall);
            }
        });
    } else {
        otherRecalls.push(...recalls);
    }

    return (
        <div className="space-y-12">
            {/* Hero / Search Section */}
            <section className="space-y-4 max-w-2xl mx-auto text-center py-8">
                <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                    Stay safe. Stay informed.
                </h2>
                <p className="text-lg text-muted-foreground">
                    A unified view of verified safety recalls in the US and India.
                </p>

                <form className="relative mt-6" action="/">
                    <input
                        name="q"
                        type="text"
                        defaultValue={query}
                        placeholder="Search products, brands, or categories..."
                        className="w-full h-12 px-4 rounded-lg border border-input bg-background shadow-sm focus:ring-2 focus:ring-accent focus:border-accent transition-all outline-none"
                    />
                    <button type="submit" className="absolute right-3 top-3 text-muted-foreground hover:text-foreground">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    </button>
                </form>
            </section>

            {/* Filter Bar */}
            <div className="pb-4">
                <FilterBar />
            </div>



            {/* India Context Helper */}
            {region === 'IN' && (
                <div className="mx-auto max-w-2xl bg-amber-500/10 border border-amber-500/20 p-3 rounded-md flex gap-3 text-sm text-amber-600/90 items-start">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 flex-shrink-0 mt-0.5">
                        <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clipRule="evenodd" />
                    </svg>
                    <span>
                        <strong>India Safety Context:</strong> Includes regulatory actions (seizures, licence cancellations) and investigation probes. Not all issues are formally labeled as "recalls".
                    </span>
                </div>
            )}

            {/* SECTION 1: Matches your tracking */}
            {watchlist && watchlist.length > 0 && (
                <div className="space-y-6">
                    <div className="flex items-center gap-2 border-b pb-2">
                        <h3 className="text-xl font-bold tracking-tight text-accent/90">Matches your tracking</h3>
                        {trackedRecalls.length > 0 && (
                            <span className="bg-accent/10 text-accent text-xs font-bold px-2 py-0.5 rounded-full">{trackedRecalls.length}</span>
                        )}
                    </div>

                    {trackedRecalls.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {trackedRecalls.map((item: Recall) => (
                                <RecallCard key={item.id} isTracked={true} item={{
                                    id: item.id.toString(),
                                    title: item.title,
                                    brand: item.brand || "Unknown Brand",
                                    date: new Date(item.published_date || item.updated_at).toLocaleDateString(undefined, { year: 'numeric', month: '2-digit', day: '2-digit' }),
                                    status: item.confidence_level.toLowerCase() as any,
                                    signal_type: item.signal_type,
                                    hazard: item.hazard_summary?.substring(0, 100) + "..."
                                }} />
                            ))}
                        </div>
                    ) : (
                        <div className="py-8 text-center bg-secondary/10 rounded-lg border border-dashed border-border/40">
                            <p className="text-sm text-muted-foreground">No verified alerts related to your tracked items right now.</p>
                        </div>
                    )}
                </div>
            )}

            {/* SECTION 2: General Recalls */}
            <div className="space-y-6">

                {/* Result Summary & Chips (User Feedback) */}
                {(region || status.length > 0 || signalType.length > 0 || params.start_date) && (
                    <div className="flex flex-col gap-2 border-b border-border/40 pb-4">
                        <p className="text-sm font-medium text-muted-foreground">
                            Showing <span className="text-foreground font-bold">{otherRecalls.length + trackedRecalls.length}</span> alerts matching your filters:
                        </p>

                        {/* Active Chips Row */}
                        <div className="flex flex-wrap gap-2">
                            {/* Region Chip */}
                            {region && (
                                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20">
                                    {region === 'IN' ? '🇮🇳 India Only' : region === 'US' ? '🇺🇸 US Only' : region}
                                </span>
                            )}

                            {/* Date Chip */}
                            {params.start_date && (
                                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-background border border-border text-foreground">
                                    📅 {new Date(params.start_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} - {params.end_date ? new Date(params.end_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : 'Now'}
                                </span>
                            )}

                            {/* Status Chips */}
                            {status.map(s => (
                                <span key={s} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-background border border-border text-foreground capitalize">
                                    {s.toLowerCase()}
                                </span>
                            ))}

                            {/* Signal Chips */}
                            {signalType.map(s => (
                                <span key={s} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-background border border-border text-foreground">
                                    {s}
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Fallback Header if no specific filters but watchlist exists */}
                {!region && status.length === 0 && trackedRecalls.length > 0 && (
                    <div className="flex items-center gap-2 border-b pb-2">
                        <h3 className="text-lg font-semibold tracking-tight text-muted-foreground">Showing the latest verified safety recalls</h3>
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {otherRecalls.map((item: Recall) => (
                        <RecallCard key={item.id} item={{
                            id: item.id.toString(),
                            title: item.title,
                            brand: item.brand || "Unknown Brand",
                            date: new Date(item.published_date || item.updated_at).toLocaleDateString(undefined, { year: 'numeric', month: '2-digit', day: '2-digit' }),
                            status: item.confidence_level.toLowerCase() as any,
                            signal_type: item.signal_type,
                            hazard: item.hazard_summary?.substring(0, 100) + "..."
                        }} />
                    ))}
                </div>
            </div>

            {recalls.length === 0 && (
                <div className="text-center py-12 text-muted-foreground">
                    {query ? (
                        <p>No matches found for "{query}".</p>
                    ) : (
                        <div className="space-y-2">
                            <p>No recent recalls running in the system.</p>
                            <p className="text-sm">Run the ingestion pipeline to fetch new data.</p>
                        </div>
                    )}
                </div>
            )}

            {!query && recalls.length > 0 && trackedRecalls.length === 0 && (
                <div className="mt-8 text-center">
                    <p className="text-sm text-muted-foreground">Showing the latest verified safety recalls.</p>
                </div>
            )}
        </div >
    );
}
