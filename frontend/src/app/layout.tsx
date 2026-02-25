import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "RedAlert | Product Recall Hub",
    description: "Aggregated safety recalls for India and US markets.",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <div className="flex flex-col min-h-screen bg-background text-foreground">
                    {/* Header / Navbar */}
                    <header className="border-b bg-card">
                        <div className="container mx-auto py-4 flex items-center justify-between">
                            <h1 className="text-xl font-semibold tracking-tight">RedAlert</h1>
                            {/* Placeholder for nav items */}
                            <nav className="text-sm text-muted-foreground flex gap-4">
                                <a href="/alerts" className="hover:text-foreground transition-colors">My Alerts</a>
                                <a href="/" className="hover:text-foreground transition-colors">Search</a>
                            </nav>
                        </div>
                    </header>

                    {/* Main Content Area */}
                    <main className="flex-1 container mx-auto py-8">
                        {children}
                    </main>

                    {/* Footer */}
                    <footer className="border-t py-6 text-center text-sm text-muted-foreground">
                        <div className="container mx-auto">
                            <p className="opacity-60">Aggregates public safety information. Always follow official manufacturer or government instructions.</p>
                            <p className="mt-2 opacity-30">© 2026 RedAlert</p>
                        </div>
                    </footer>
                </div>
            </body>
        </html>
    );
}
