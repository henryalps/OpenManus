import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <section className="rounded-xl border border-canvas-border bg-canvas-panel p-8">
        <h1 className="max-w-2xl text-2xl font-semibold leading-tight text-ink">
          Walk into a client meeting with an accurate mockup <span className="text-brand">and</span> a price — in under 10 minutes.
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-relaxed text-ink-muted">
          Brand Factory Studio composites client logos onto real AMROD product variants and (next phase) prices them
          in USD from ZAR cost. Built on a swappable data provider, so live AMROD access drops in without changing a thing.
        </p>
        <div className="mt-5 flex gap-3">
          <Link href="/mockup" className="rounded-lg bg-brand px-4 py-2 text-sm font-medium text-white hover:bg-brand-deep">
            Open mockup studio
          </Link>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        {[
          { n: "1", t: "Mockup engine", s: "Live now", d: "Locked-overlay compositing with flat, mug, and cap warps. No generative AI — pixels in = pixels out.", on: true },
          { n: "2", t: "Pricing engine", s: "Next", d: "ZAR → USD at your effective rate, +25% import on the full invoice, banded markup, rounding.", on: false },
          { n: "3", t: "Catalogue & quotes", s: "Then", d: "Per-client branded catalogue with each mockup and price — PDF and shareable link.", on: false },
        ].map((c) => (
          <div key={c.n} className="rounded-xl border border-canvas-border bg-canvas-panel p-5">
            <div className="flex items-center justify-between">
              <span className="grid h-7 w-7 place-items-center rounded-lg bg-canvas-panel2 text-sm font-semibold text-ink-muted">{c.n}</span>
              <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${c.on ? "bg-ok/15 text-ok" : "bg-canvas-panel2 text-ink-faint"}`}>{c.s}</span>
            </div>
            <h3 className="mt-3 text-sm font-semibold text-ink">{c.t}</h3>
            <p className="mt-1 text-xs leading-relaxed text-ink-muted">{c.d}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
