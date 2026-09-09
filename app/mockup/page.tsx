"use client";

import dynamic from "next/dynamic";

// Konva needs the browser — load the studio client-side only.
const MockupStudio = dynamic(() => import("@/components/mockup/MockupStudio"), {
  ssr: false,
  loading: () => <div className="py-20 text-center text-sm text-ink-faint">Loading studio…</div>,
});

export default function MockupPage() {
  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-lg font-semibold text-ink">Mockup studio</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Place a client logo as a locked overlay on the exact colour variant. Define each print zone once per product; reuse across colours.
        </p>
      </div>
      <MockupStudio />
    </div>
  );
}
