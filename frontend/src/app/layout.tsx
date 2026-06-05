import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { CookieBanner } from "@/components/ui/CookieBanner";
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
                            <Link href="/">
                                <h1 className="text-xl font-semibold tracking-tight hover:text-primary transition-colors cursor-pointer">RedAlert</h1>
                            </Link>
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
                    <footer className="border-t py-8 text-sm text-muted-foreground bg-card">
                        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between gap-6">
                            <div className="flex-1">
                                <h3 className="font-semibold text-foreground mb-2">RedAlert</h3>
                                <p className="opacity-80 mb-2">
                                    Disclaimer: RedAlert aggregates public safety and product recall information. This is a tool for informational purposes only. We do not guarantee the accuracy, completeness, or timeliness of the data. Always follow official manufacturer or government instructions. You are solely responsible for actions taken based on this information.
                                </p>
                            </div>
                            
                            <div>
                                <h4 className="font-semibold text-foreground mb-2">Legal & Compliance</h4>
                                <ul className="space-y-1 opacity-80">
                                    <li><a href="/privacy" className="hover:text-foreground hover:underline">Privacy Policy</a></li>
                                    <li><a href="/terms" className="hover:text-foreground hover:underline">Terms of Service</a></li>
                                    <li><a href="/compliance" className="hover:text-foreground hover:underline">Compliance & Data Sources</a></li>
                                </ul>
                            </div>

                            <div>
                                <h4 className="font-semibold text-foreground mb-2">Contact</h4>
                                <ul className="space-y-1 opacity-80">
                                    <li><a href="mailto:bipulnandan276@gmail.com" className="hover:text-foreground hover:underline">bipulnandan276@gmail.com</a></li>
                                </ul>
                            </div>
                        </div>
                        <div className="container mx-auto px-4 mt-8 pt-4 border-t border-border/50 text-center opacity-60">
                            <p>© {new Date().getFullYear()} RedAlert. All rights reserved.</p>
                        </div>
                    </footer>
                    <CookieBanner />
                </div>
            </body>
        </html>
    );
}
