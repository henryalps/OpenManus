import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Brand Factory Studio",
  description: "Mockups and priced quotes for branded merchandise — in minutes.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="sticky top-0 z-10 border-b border-canvas-border bg-canvas-bg/80 backdrop-blur">
          <div className="mx-auto flex max-w-[1400px] items-center justify-between px-5 py-3">
            <div className="flex items-center gap-2.5">
              <span className="grid h-7 w-7 place-items-center rounded-lg bg-brand text-sm font-bold text-white">BF</span>
              <div className="leading-tight">
                <div className="text-sm font-semibold text-ink">Brand Factory Studio</div>
                <div className="text-[11px] text-ink-faint">Harare · AMROD sourcing</div>
              </div>
            </div>
            <nav className="flex items-center gap-1 text-sm">
              <a href="/" className="rounded-lg px-3 py-1.5 text-ink-muted hover:bg-canvas-hover hover:text-ink">Home</a>
              <a href="/mockup" className="rounded-lg px-3 py-1.5 text-ink-muted hover:bg-canvas-hover hover:text-ink">Mockup studio</a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-[1400px] px-5 py-6">{children}</main>
      </body>
    </html>
  );
}
