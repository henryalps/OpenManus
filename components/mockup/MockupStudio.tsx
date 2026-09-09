"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Stage, Layer, Image as KImage, Rect, Transformer, Text, Group } from "react-konva";
import type Konva from "konva";
import useImage from "use-image";

import { getProvider } from "@/lib/providers";
import type { Branding, Colour, Product, Variant } from "@/lib/providers/types";
import type { MockupTemplate, PrintZone } from "@/lib/mockup/types";
import { getOrInitTemplate, saveTemplate, newZone } from "@/lib/mockup/templates";
import { warpLogo } from "@/lib/mockup/warp";
import { exportStagePng, downloadDataUrl } from "@/lib/mockup/export";
import { Panel, Button, Slider, Segmented, Swatch, Badge } from "@/components/ui";

const STAGE_MAX = 640;

interface Logo {
  src: string;
  img: HTMLImageElement;
  w: number;
  h: number;
}

interface Xf {
  x: number; // stage px, center
  y: number;
  scale: number;
  rotation: number;
  opacity: number;
  blend: "normal" | "multiply";
  curvature: number;
}

const defaultXf = (): Xf => ({ x: 0, y: 0, scale: 1, rotation: 0, opacity: 1, blend: "normal", curvature: 0.5 });

/** Contain-fit a w×h box inside the stage, centred. */
function containRect(imgW: number, imgH: number, stageW: number, stageH: number) {
  if (!imgW || !imgH) return { x: 0, y: 0, w: stageW, h: stageH };
  const s = Math.min(stageW / imgW, stageH / imgH);
  const w = imgW * s;
  const h = imgH * s;
  return { x: (stageW - w) / 2, y: (stageH - h) / 2, w, h };
}

export default function MockupStudio() {
  const provider = getProvider();

  const [products, setProducts] = useState<Product[]>([]);
  const [colours, setColours] = useState<Record<string, Colour>>({});
  const [productCode, setProductCode] = useState<string>("");
  const [variants, setVariants] = useState<Variant[]>([]);
  const [fullCode, setFullCode] = useState<string>("");
  const [branding, setBranding] = useState<Branding | null>(null);

  const [template, setTemplate] = useState<MockupTemplate | null>(null);
  const [activeZoneId, setActiveZoneId] = useState<string>("");
  const [mode, setMode] = useState<"place" | "zones">("place");

  const [logo, setLogo] = useState<Logo | null>(null);
  const [xf, setXf] = useState<Xf>(defaultXf());
  const [dirty, setDirty] = useState(false);

  const [stageSize, setStageSize] = useState(STAGE_MAX);
  const wrapRef = useRef<HTMLDivElement>(null);
  const stageRef = useRef<Konva.Stage>(null);
  const logoNodeRef = useRef<Konva.Image>(null);
  const zoneNodeRef = useRef<Konva.Rect>(null);
  const trRef = useRef<Konva.Transformer>(null);

  // ---- data load ---------------------------------------------------------
  useEffect(() => {
    (async () => {
      const [ps, cs] = await Promise.all([provider.getProducts(), provider.getColourSwatches()]);
      setProducts(ps);
      setColours(Object.fromEntries(cs.map((c) => [c.code, c])));
      if (ps[0]) setProductCode(ps[0].code);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!productCode) return;
    (async () => {
      const [vs, br] = await Promise.all([provider.getVariants(productCode), provider.getBranding(productCode)]);
      setVariants(vs);
      setBranding(br);
      setFullCode(vs[0]?.fullCode ?? "");
      const tpl = getOrInitTemplate(productCode, br);
      setTemplate(tpl);
      setActiveZoneId(tpl.zones[0]?.id ?? "");
      setDirty(false);
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [productCode]);

  // ---- responsive stage --------------------------------------------------
  useEffect(() => {
    const measure = () => {
      const w = wrapRef.current?.clientWidth ?? STAGE_MAX;
      setStageSize(Math.min(STAGE_MAX, Math.max(360, w)));
    };
    measure();
    const ro = new ResizeObserver(measure);
    if (wrapRef.current) ro.observe(wrapRef.current);
    return () => ro.disconnect();
  }, []);

  const variant = variants.find((v) => v.fullCode === fullCode) ?? null;
  const productImageUrl = variant?.images.find((i) => i.isPrimary)?.url ?? variant?.images[0]?.url ?? "";
  const [productImg] = useImage(productImageUrl, "anonymous");

  const imageRect = useMemo(
    () => containRect(productImg?.width ?? 1, productImg?.height ?? 1, stageSize, stageSize),
    [productImg, stageSize],
  );

  const zones = template?.zones ?? [];
  const activeZone = zones.find((z) => z.id === activeZoneId) ?? null;

  // Zone rectangle in stage pixels.
  const zonePx = useCallback(
    (z: PrintZone) => ({
      x: imageRect.x + z.x * imageRect.w,
      y: imageRect.y + z.y * imageRect.h,
      w: z.width * imageRect.w,
      h: z.height * imageRect.h,
    }),
    [imageRect],
  );

  // Base (fit-to-zone) size of the logo for the active zone.
  const logoBase = useMemo(() => {
    if (!logo || !activeZone) return null;
    const zp = zonePx(activeZone);
    const fit = Math.min(zp.w / logo.w, zp.h / logo.h);
    return { w: logo.w * fit, h: logo.h * fit, zp };
  }, [logo, activeZone, zonePx]);

  // When a logo is dropped, or zone/variant changes, recentre it on the zone.
  useEffect(() => {
    if (logoBase && activeZone) {
      setXf((p) => ({ ...p, x: logoBase.zp.x + logoBase.zp.w / 2, y: logoBase.zp.y + logoBase.zp.h / 2 }));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [logo, activeZoneId]);

  // Warped raster for non-flat zones (deterministic geometric remap of the logo).
  const warpedCanvas = useMemo(() => {
    if (!logo || !activeZone || !logoBase || activeZone.warp === "flat") return null;
    const pre = document.createElement("canvas");
    pre.width = Math.max(2, Math.round(logoBase.w));
    pre.height = Math.max(2, Math.round(logoBase.h));
    pre.getContext("2d")!.drawImage(logo.img, 0, 0, pre.width, pre.height);
    return warpLogo(pre, activeZone.warp, xf.curvature);
  }, [logo, activeZone, logoBase, xf.curvature]);

  // ---- transformer wiring ------------------------------------------------
  useEffect(() => {
    const tr = trRef.current;
    if (!tr) return;
    const node = mode === "zones" ? zoneNodeRef.current : logoNodeRef.current;
    tr.nodes(node && (mode === "place" ? !!logo : true) ? [node] : []);
    tr.getLayer()?.batchDraw();
  }, [mode, logo, activeZoneId, fullCode, warpedCanvas]);

  // ---- handlers ----------------------------------------------------------
  const onUpload = (file: File) => {
    const src = URL.createObjectURL(file);
    const img = new window.Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
      setLogo({ src, img, w: img.naturalWidth || 300, h: img.naturalHeight || 300 });
      setXf(defaultXf());
    };
    img.src = src;
  };

  const fitToZone = () => setXf((p) => ({ ...p, scale: 1, rotation: 0 }));

  const updateZone = (patch: Partial<PrintZone>) => {
    if (!template || !activeZone) return;
    setTemplate({
      ...template,
      zones: template.zones.map((z) => (z.id === activeZone.id ? { ...z, ...patch } : z)),
    });
    setDirty(true);
  };

  const addZone = () => {
    if (!template) return;
    const z = newZone(`Zone ${template.zones.length + 1}`);
    setTemplate({ ...template, zones: [...template.zones, z] });
    setActiveZoneId(z.id);
    setDirty(true);
  };

  const deleteZone = () => {
    if (!template || template.zones.length <= 1) return;
    const remaining = template.zones.filter((z) => z.id !== activeZoneId);
    setTemplate({ ...template, zones: remaining });
    setActiveZoneId(remaining[0].id);
    setDirty(true);
  };

  const persist = () => {
    if (!template) return;
    saveTemplate(template);
    setDirty(false);
  };

  const exportPng = () => {
    const stage = stageRef.current;
    if (!stage) return;
    // Hide chrome (zone outlines, transformer) for a clean proof.
    const prev = mode;
    setMode("place");
    requestAnimationFrame(() => {
      const url = exportStagePng(stage, 2000);
      downloadDataUrl(url, `${fullCode || productCode}-mockup.png`);
      setMode(prev);
    });
  };

  const product = products.find((p) => p.code === productCode);

  // ---- render ------------------------------------------------------------
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-[260px_minmax(0,1fr)_280px]">
      {/* LEFT: product + colour picker */}
      <div className="flex flex-col gap-4">
        <Panel title="Product">
          <select
            value={productCode}
            onChange={(e) => setProductCode(e.target.value)}
            className="w-full rounded-lg border border-canvas-border bg-canvas-bg px-2.5 py-2 text-sm text-ink"
          >
            {products.map((p) => (
              <option key={p.code} value={p.code}>
                {p.name}
              </option>
            ))}
          </select>
          {product && <p className="mt-2 text-xs text-ink-faint">{product.code}</p>}
        </Panel>

        <Panel title="Colour variant">
          <div className="flex flex-col gap-1">
            {variants.map((v) => {
              const c = colours[v.colourCode];
              const active = v.fullCode === fullCode;
              return (
                <button
                  key={v.fullCode}
                  onClick={() => setFullCode(v.fullCode)}
                  className={`flex items-center gap-2 rounded-lg px-2 py-1.5 text-left text-sm transition-colors ${
                    active ? "bg-canvas-hover text-ink" : "text-ink-muted hover:bg-canvas-hover/60"
                  }`}
                >
                  <Swatch hex={c?.hex ?? "#888"} title={c?.name} />
                  <span className="flex-1">{c?.name ?? v.colourCode}{v.size && v.size !== "OS" ? ` · ${v.size}` : ""}</span>
                  <span className="font-mono text-[11px] text-ink-faint">{v.fullCode}</span>
                </button>
              );
            })}
          </div>
        </Panel>

        <Panel title="Client logo">
          <label className="block cursor-pointer rounded-lg border border-dashed border-canvas-border bg-canvas-bg px-3 py-4 text-center text-xs text-ink-muted hover:border-brand hover:text-ink">
            {logo ? "Replace logo (PNG / SVG)" : "Upload logo (PNG / SVG)"}
            <input
              type="file"
              accept="image/png,image/svg+xml,image/*"
              className="hidden"
              onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
            />
          </label>
          {logo && (
            <div className="mt-2 flex items-center gap-2">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={logo.src} alt="logo" className="h-8 w-8 rounded bg-white/5 object-contain p-0.5" />
              <span className="text-[11px] text-ink-faint">{logo.w}×{logo.h}px</span>
            </div>
          )}
        </Panel>
      </div>

      {/* CENTER: canvas */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <Segmented
            value={mode}
            onChange={setMode}
            options={[
              { value: "place", label: "Place logo" },
              { value: "zones", label: "Define zones" },
            ]}
          />
          <Badge tone="ok">🔒 Locked overlay · compositing only</Badge>
        </div>

        <div ref={wrapRef} className="flex items-center justify-center rounded-xl border border-canvas-border bg-[repeating-conic-gradient(#171c23_0%_25%,#11151b_0%_50%)] bg-[length:24px_24px] p-2">
          <Stage ref={stageRef} width={stageSize} height={stageSize}>
            <Layer>
              {/* product photo — locked background */}
              {productImg && (
                <KImage image={productImg} x={imageRect.x} y={imageRect.y} width={imageRect.w} height={imageRect.h} listening={false} />
              )}

              {/* zone outlines */}
              {zones.map((z) => {
                const zp = zonePx(z);
                const isActive = z.id === activeZoneId;
                return (
                  <Group key={z.id}>
                    <Rect
                      ref={isActive && mode === "zones" ? zoneNodeRef : undefined}
                      x={zp.x}
                      y={zp.y}
                      width={zp.w}
                      height={zp.h}
                      rotation={z.rotationDeg}
                      stroke={isActive ? "#ff6b2c" : "#9aa7b4"}
                      strokeWidth={isActive ? 1.5 : 1}
                      dash={[6, 4]}
                      opacity={mode === "zones" || isActive ? 0.9 : 0.25}
                      draggable={mode === "zones" && isActive}
                      onClick={() => setActiveZoneId(z.id)}
                      onTap={() => setActiveZoneId(z.id)}
                      onDragEnd={(e) => {
                        updateZone({
                          x: (e.target.x() - imageRect.x) / imageRect.w,
                          y: (e.target.y() - imageRect.y) / imageRect.h,
                        });
                      }}
                      onTransformEnd={(e) => {
                        const node = e.target as Konva.Rect;
                        const w = node.width() * node.scaleX();
                        const h = node.height() * node.scaleY();
                        node.scaleX(1);
                        node.scaleY(1);
                        updateZone({
                          x: (node.x() - imageRect.x) / imageRect.w,
                          y: (node.y() - imageRect.y) / imageRect.h,
                          width: w / imageRect.w,
                          height: h / imageRect.h,
                          rotationDeg: node.rotation(),
                        });
                      }}
                    />
                    <Text x={zp.x} y={zp.y - 14} text={z.name} fontSize={11} fill={isActive ? "#ff6b2c" : "#9aa7b4"} listening={false} />
                  </Group>
                );
              })}

              {/* logo overlay — flat (native) or warped raster */}
              {logo && logoBase && activeZone && (
                <KImage
                  ref={logoNodeRef}
                  image={activeZone.warp === "flat" ? logo.img : warpedCanvas ?? logo.img}
                  x={xf.x}
                  y={xf.y}
                  width={logoBase.w}
                  height={logoBase.h}
                  offsetX={logoBase.w / 2}
                  offsetY={logoBase.h / 2}
                  scaleX={xf.scale}
                  scaleY={xf.scale}
                  rotation={xf.rotation + (activeZone.rotationDeg || 0)}
                  opacity={xf.opacity}
                  globalCompositeOperation={xf.blend === "multiply" ? "multiply" : "source-over"}
                  draggable={mode === "place"}
                  onClick={() => setMode("place")}
                  onDragEnd={(e) => setXf((p) => ({ ...p, x: e.target.x(), y: e.target.y() }))}
                  onTransformEnd={(e) => {
                    const node = e.target as Konva.Image;
                    setXf((p) => ({
                      ...p,
                      x: node.x(),
                      y: node.y(),
                      scale: node.scaleX(),
                      rotation: node.rotation() - (activeZone.rotationDeg || 0),
                    }));
                  }}
                />
              )}

              {(mode === "zones" || (mode === "place" && logo)) && (
                <Transformer
                  ref={trRef}
                  rotateEnabled
                  keepRatio={mode === "place"}
                  enabledAnchors={
                    mode === "place"
                      ? ["top-left", "top-right", "bottom-left", "bottom-right"]
                      : ["top-left", "top-right", "bottom-left", "bottom-right", "middle-left", "middle-right", "top-center", "bottom-center"]
                  }
                  borderStroke="#ff6b2c"
                  anchorStroke="#ff6b2c"
                  anchorFill="#161b22"
                  anchorSize={8}
                />
              )}
            </Layer>
          </Stage>
        </div>

        <div className="flex items-center justify-between">
          <p className="text-xs text-ink-faint">
            {mode === "place"
              ? "Drag, scale, and rotate the logo. It's locked — pixels never change."
              : "Drag and resize the dashed print zone, then save the template."}
          </p>
          <div className="flex gap-2">
            {mode === "zones" && (
              <Button size="sm" variant={dirty ? "primary" : "default"} onClick={persist} title="Save zone template">
                {dirty ? "Save template *" : "Saved"}
              </Button>
            )}
            <Button size="sm" variant="primary" onClick={exportPng} disabled={!logo}>
              Export PNG
            </Button>
          </div>
        </div>
      </div>

      {/* RIGHT: controls */}
      <div className="flex flex-col gap-4">
        {mode === "place" ? (
          <Panel title="Logo placement">
            {!logo ? (
              <p className="text-xs text-ink-faint">Upload a logo to start placing it.</p>
            ) : (
              <div className="flex flex-col gap-3.5">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-ink-muted">Active zone</span>
                  <select
                    value={activeZoneId}
                    onChange={(e) => setActiveZoneId(e.target.value)}
                    className="rounded-lg border border-canvas-border bg-canvas-bg px-2 py-1 text-xs text-ink"
                  >
                    {zones.map((z) => (
                      <option key={z.id} value={z.id}>{z.name}</option>
                    ))}
                  </select>
                </div>
                <Slider label="Scale" min={0.1} max={3} step={0.01} value={xf.scale} onChange={(v) => setXf((p) => ({ ...p, scale: v }))} />
                <Slider label="Rotation" min={-180} max={180} value={xf.rotation} suffix="°" onChange={(v) => setXf((p) => ({ ...p, rotation: v }))} />
                <Slider label="Opacity" min={0.1} max={1} step={0.01} value={xf.opacity} onChange={(v) => setXf((p) => ({ ...p, opacity: v }))} />
                {activeZone && activeZone.warp !== "flat" && (
                  <Slider label={`Wrap (${activeZone.warp})`} min={0} max={1} step={0.01} value={xf.curvature} onChange={(v) => setXf((p) => ({ ...p, curvature: v }))} />
                )}
                <div>
                  <div className="mb-1 text-xs text-ink-muted">Ink blend</div>
                  <Segmented
                    value={xf.blend}
                    onChange={(v) => setXf((p) => ({ ...p, blend: v }))}
                    options={[
                      { value: "normal", label: "Normal" },
                      { value: "multiply", label: "Multiply" },
                    ]}
                  />
                </div>
                <Button size="sm" variant="ghost" onClick={fitToZone}>Reset to zone fit</Button>
              </div>
            )}
          </Panel>
        ) : (
          <Panel title="Zone template" right={<Button size="sm" variant="ghost" onClick={addZone}>+ Zone</Button>}>
            {activeZone ? (
              <div className="flex flex-col gap-3.5">
                <label className="block">
                  <div className="mb-1 text-xs text-ink-muted">Name</div>
                  <input
                    value={activeZone.name}
                    onChange={(e) => updateZone({ name: e.target.value })}
                    className="w-full rounded-lg border border-canvas-border bg-canvas-bg px-2.5 py-1.5 text-sm text-ink"
                  />
                </label>
                <div>
                  <div className="mb-1 text-xs text-ink-muted">Warp</div>
                  <Segmented
                    value={activeZone.warp}
                    onChange={(v) => updateZone({ warp: v })}
                    options={[
                      { value: "flat", label: "Flat" },
                      { value: "cylindrical", label: "Mug" },
                      { value: "curved", label: "Cap" },
                    ]}
                  />
                </div>
                <Slider label="Rotation" min={-45} max={45} value={activeZone.rotationDeg} suffix="°" onChange={(v) => updateZone({ rotationDeg: v })} />
                <p className="text-[11px] leading-relaxed text-ink-faint">
                  Defined once per product in normalized coordinates — reused across every colour variant.
                </p>
                <Button size="sm" variant="danger" onClick={deleteZone} disabled={zones.length <= 1}>Delete zone</Button>
              </div>
            ) : (
              <p className="text-xs text-ink-faint">No zone selected.</p>
            )}
          </Panel>
        )}

        <Panel title="Proof details">
          <dl className="space-y-1.5 text-xs">
            <div className="flex justify-between"><dt className="text-ink-faint">Variant</dt><dd className="font-mono text-ink">{fullCode || "—"}</dd></div>
            <div className="flex justify-between"><dt className="text-ink-faint">Zone</dt><dd className="text-ink">{activeZone?.name ?? "—"}</dd></div>
            <div className="flex justify-between"><dt className="text-ink-faint">Method warp</dt><dd className="text-ink capitalize">{activeZone?.warp ?? "—"}</dd></div>
            <div className="flex justify-between"><dt className="text-ink-faint">Data source</dt><dd className="text-ink">{provider.name}</dd></div>
          </dl>
        </Panel>
      </div>
    </div>
  );
}
