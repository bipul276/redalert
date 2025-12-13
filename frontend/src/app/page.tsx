import { RecallCard } from "@/components/ui/RecallCard";
import { fetchRecalls, Recall } from "@/lib/api";
import { fetchWatchlists, WatchlistItem } from "@/lib/api_watchlist";

export default async function Home({ searchParams }: { searchParams: Promise<{ q?: string; region?: string }> }) {
    const params = await searchParams;
    const query = params.q;
    const region = params.region;

    // Parallel fetch for recalls and watchlist
    const [recalls, watchlist] = await Promise.all([
        fetchRecalls(region, query),
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

            {/* Filters (Neutral/Polished UI) */}
            <div className="flex flex-wrap gap-3 justify-center">
                <a href="/" className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${!region ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/20' : 'bg-secondary/50 text-muted-foreground hover:bg-secondary hover:text-foreground'}`}>All Regions</a>
                <a href="/?region=US" className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${region === 'US' ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/20' : 'bg-secondary/50 text-muted-foreground hover:bg-secondary hover:text-foreground'}`}>US Only</a>
                <a href="/?region=IN" className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${region === 'IN' ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/20' : 'bg-secondary/50 text-muted-foreground hover:bg-secondary hover:text-foreground'}`}>India Only</a>
            </div>

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
                                    date: new Date(item.updated_at).toLocaleDateString(),
                                    status: item.confidence_level.toLowerCase() as any,
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
                {watchlist && watchlist.length > 0 && (
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
                            date: new Date(item.updated_at).toLocaleDateString(),
                            status: item.confidence_level.toLowerCase() as any,
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
