import React from 'react';

type BadgeVariant = 'default' | 'confirmed' | 'probable' | 'watch';

interface BadgeProps {
    children: React.ReactNode;
    variant?: BadgeVariant;
}

const styles: Record<BadgeVariant, string> = {
    default: "bg-secondary text-secondary-foreground",
    confirmed: "bg-[hsl(var(--status-confirmed))] text-red-950", // Muted red bg, dark text
    probable: "bg-[hsl(var(--status-probable))] text-amber-950",
    watch: "bg-[hsl(var(--status-watch))] text-zinc-900",
};

export function Badge({ children, variant = 'default' }: BadgeProps) {
    return (
        <span className={`inline-flex items-center justify-center rounded-full px-2.5 h-5 text-[10px] uppercase tracking-[0.2em] font-bold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 ${styles[variant]}`}>
            {children}
        </span>
    );
}
