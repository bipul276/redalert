"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export function CookieBanner() {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        // Check if user has already consented
        const hasConsented = localStorage.getItem("cookie_consent");
        if (!hasConsented) {
            setIsVisible(true);
        }
    }, []);

    const handleAccept = () => {
        localStorage.setItem("cookie_consent", "true");
        setIsVisible(false);
    };

    if (!isVisible) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-card border-t border-border p-4 shadow-lg z-50">
            <div className="container mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="text-sm text-muted-foreground flex-1">
                    We use cookies and similar technologies (including from third-party partners like Google) to analyze site traffic and serve personalized ads. By continuing to use our site, you agree to our use of cookies as described in our{" "}
                    <Link href="/privacy" className="text-foreground underline font-medium hover:text-primary">
                        Privacy Policy
                    </Link>.
                </div>
                <div className="flex gap-3 flex-shrink-0">
                    <button
                        onClick={handleAccept}
                        className="bg-primary text-primary-foreground px-5 py-2 rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
                    >
                        Accept & Continue
                    </button>
                </div>
            </div>
        </div>
    );
}
