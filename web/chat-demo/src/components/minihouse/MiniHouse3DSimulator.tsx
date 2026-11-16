import { useEffect, useRef, useState } from 'react'

export type SimulationMode = 'top-lift' | 'inset-support' | 'exploded'

export interface BomLayerItem {
  layer: number
  id: string
  name: string
  material: string
  dimensionsMm: string
  massNote: string
  status: 'CONCEPTUAL' | 'CALCULADO' | 'ENSAYADO' | 'LIBERADO'
  prompt: string
}

export const MINIHOUSE_BOM_LAYERS: BomLayerItem[] = [
  {
    layer: 4,
    id: 'MH-ROF-004',
    name: 'Roof & Glazing Assembly',
    material: 'Standing-Seam Steel + Triple Glazing (U ≈ 0.8 W/m²K)',
    dimensionsMm: '6000 × 3000 × 450 mm',
    massNote: 'Pending Phase 1 inventory',
    status: 'CONCEPTUAL',
    prompt:
      'Analyze how roof & window frame racking deformation is controlled during a 4-point crane lift of the 6000×3000 mm MiniHouse module.',
  },
  {
    layer: 3,
    id: 'MH-ENV-003',
    name: 'Reclaimed Timber Wall Panels',
    material: 'Repurposed Nordic Barn Cladding (Documented Batch)',
    dimensionsMm: '2750 mm clear height · ventilated rain-screen',
    massNote: 'Weighed per panel batch (Phase 1)',
    status: 'CONCEPTUAL',
    prompt:
      'What moisture drainage, corrosion isolation, and traceability records are required when mounting reclaimed timber cladding onto the MiniHouse steel frame?',
  },
  {
    layer: 2,
    id: 'MH-NOD-002',
    name: 'Corner Posts & Rigging Lugs',
    material: 'RHS Steel Posts + EN 13155 Padeyes / ISO-style Corner Nodes',
    dimensionsMm: '4 × Corner Columns (H = 3200 mm)',
    massNote: 'Moment-resisting / pinned comparison',
    status: 'CONCEPTUAL',
    prompt:
      'Compare top-corner lifting vs. base sling lifting (with spreader bar) for the 6×3 m MiniHouse corner nodes under EN 13155 and NS-EN 1993-1-8.',
  },
  {
    layer: 1,
    id: 'MH-STR-001',
    name: 'Primary Steel Skid & Crossmembers',
    material: '2 × 6000 mm Longitudinal Beams + 5 × 3000 mm Crossmembers (S355)',
    dimensionsMm: '6000 × 3000 mm base footprint',
    massNote: 'Hypothetical test case: 3000 kg total (q = 2.4525 kN/m)',
    status: 'CALCULADO',
    prompt:
      'Show the Euler-Bernoulli derivation comparing end supports (24.63 mm deflection) vs. 1.2 m inset supports (1.49 mm deflection) for the 6 m MiniHouse longitudinal beams.',
  },
]

/**
 * Computes Euler-Bernoulli deflection w(x) in mm along a symmetric 6.0 m beam
 * with uniform load q = 2.4525 kN/m and flexural rigidity EI = 1.68 MN·m²,
 * supported symmetrically at distance `a` (meters) from both ends.
 * Positive return value = downward sag (mm).
 */
export function computeBeamDeflectionMm(xMeters: number, insetMeters: number): number {
  const L = 6.0
  const q = 2452.5 // N/m
  const EI = 1.68e6 // N·m²
  const a = Math.max(0, Math.min(1.8, insetMeters))
  const l = L - 2 * a // central span between supports

  // Symmetry around L/2: map x to [0, L/2]
  const x = xMeters <= L / 2 ? xMeters : L - xMeters

  if (x >= a) {
    // Between the two supports: u in [0, l/2] measured from left support
    const u = x - a
    const term1 = (u * (l ** 3 - 2 * l * u ** 2 + u ** 3)) / 24
    const term2 = (a ** 2 * u * (l - u)) / 4
    return ((q / EI) * (term1 - term2)) * 1000
  } else {
    // Cantilever overhang: z = a - x in [0, a] measured outward from support
    const z = a - x
    const slopeAtSupport = (q / EI) * (l ** 3 / 24 - (a ** 2 * l) / 4)
    const cantSag = (q / EI) * ((a ** 2 * z ** 2) / 4 - (a * z ** 3) / 6 + z ** 4 / 24)
    return (-slopeAtSupport * z + cantSag) * 1000
  }
}

export function computePeakDeflectionMm(insetMeters: number): {
  midspanMm: number
  tipMm: number
  maxAbsMm: number
} {
  const midspanMm = computeBeamDeflectionMm(3.0, insetMeters)
  const tipMm = computeBeamDeflectionMm(0.0, insetMeters)
  let maxAbs = Math.max(Math.abs(midspanMm), Math.abs(tipMm))
  for (let i = 0; i <= 60; i++) {
    const d = Math.abs(computeBeamDeflectionMm((i / 60) * 6.0, insetMeters))
    if (d > maxAbs) maxAbs = d
  }
  return { midspanMm, tipMm, maxAbsMm: maxAbs }
}

function heatColor(norm: number): string {
  // Maps normalized deflection [0..1] to cyan -> green -> yellow -> magenta/red (like FEA contour)
  const t = Math.max(0, Math.min(1, norm))
  if (t < 0.33) {
    const k = t / 0.33
    const r = Math.round(20 + k * 40)
    const g = Math.round(210 + k * 40)
    const b = Math.round(235 - k * 120)
    return `rgb(${r},${g},${b})`
  }
  if (t < 0.66) {
    const k = (t - 0.33) / 0.33
    const r = Math.round(60 + k * 195)
    const g = Math.round(250 - k * 50)
    const b = Math.round(115 - k * 85)
    return `rgb(${r},${g},${b})`
  }
  const k = (t - 0.66) / 0.34
  const r = 255
  const g = Math.round(200 - k * 135)
  const b = Math.round(30 + k * 140)
  return `rgb(${r},${g},${b})`
}

export const MiniHouse3DSimulator = ({
  onAskAi,
}: {
  onAskAi: (question: string) => void
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [mode, setMode] = useState<SimulationMode>('top-lift')
  const [insetMeters, setInsetMeters] = useState<number>(1.2)
  const [explodeFactor, setExplodeFactor] = useState<number>(0)
  const [yaw, setYaw] = useState<number>(-0.62)
  const [pitch, setPitch] = useState<number>(0.42)
  const [zoom, setZoom] = useState<number>(1.0)
  const [selectedLayer, setSelectedLayer] = useState<BomLayerItem>(MINIHOUSE_BOM_LAYERS[3])
  const dragRef = useRef<{ active: boolean; x: number; y: number }>({
    active: false,
    x: 0,
    y: 0,
  })

  const effectiveInset = mode === 'top-lift' ? 0.0 : mode === 'inset-support' ? insetMeters : 1.2
  const stats = computePeakDeflectionMm(effectiveInset)

  // Smoothly animate explodeFactor when mode changes
  useEffect(() => {
    const target = mode === 'exploded' ? 1 : 0
    let raf = 0
    const step = () => {
      setExplodeFactor((prev) => {
        const diff = target - prev
        if (Math.abs(diff) < 0.01) return target
        raf = requestAnimationFrame(step)
        return prev + diff * 0.14
      })
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [mode])

  // Render interactive 3D viewport
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    const width = canvas.clientWidth || 720
    const height = canvas.clientHeight || 440
    canvas.width = width * dpr
    canvas.height = height * dpr
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

    // Dark CAD background
    ctx.fillStyle = '#11151A'
    ctx.fillRect(0, 0, width, height)

    const cx = width * 0.5
    const cy = height * (mode === 'exploded' ? 0.62 : 0.56)
    const scale = Math.min(width, height) * 0.095 * zoom

    const cosY = Math.cos(yaw)
    const sinY = Math.sin(yaw)
    const cosP = Math.cos(pitch)
    const sinP = Math.sin(pitch)

    // 3D world (meters: x in [-3, 3], y in [-1.5, 1.5], z vertical upward)
    const project = (x: number, y: number, z: number): [number, number] => {
      const rx = x * cosY - y * sinY
      const ry = x * sinY + y * cosY
      const screenX = cx + rx * scale
      const screenY = cy - z * cosP * scale + ry * sinP * scale
      return [screenX, screenY]
    }

    // Draw subtle CAD ground grid at z = -0.35
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.09)'
    ctx.lineWidth = 1
    for (let gx = -4; gx <= 4; gx += 1) {
      const [x1, y1] = project(gx, -2.5, -0.35)
      const [x2, y2] = project(gx, 2.5, -0.35)
      ctx.beginPath()
      ctx.moveTo(x1, y1)
      ctx.lineTo(x2, y2)
      ctx.stroke()
    }
    for (let gy = -2.5; gy <= 2.5; gy += 1) {
      const [x1, y1] = project(-4, gy, -0.35)
      const [x2, y2] = project(4, gy, -0.35)
      ctx.beginPath()
      ctx.moveTo(x1, y1)
      ctx.lineTo(x2, y2)
      ctx.stroke()
    }

    // Visual exaggeration factor so mm deflection is clearly visible in 3D
    const sagScale = mode === 'exploded' ? 0 : 0.011

    // Layer 1: Primary Steel Skid (6.0 m x 3.0 m)
    const zSkid = 0
    const segments = 36

    // Draw 5 crossmembers (at x = -3, -1.5, 0, 1.5, 3)
    const crossPositions = [-3, -1.5, 0, 1.5, 3]
    for (const xm of crossPositions) {
      const sag = computeBeamDeflectionMm(xm + 3, effectiveInset) * sagScale
      const [x1, y1] = project(xm, -1.5, zSkid - sag)
      const [x2, y2] = project(xm, 1.5, zSkid - sag)
      ctx.strokeStyle = mode === 'exploded' ? '#64748B' : heatColor(Math.abs(sag) / (24.63 * 0.011 || 1))
      ctx.lineWidth = xm === -3 || xm === 3 ? 6 : 4
      ctx.beginPath()
      ctx.moveTo(x1, y1)
      ctx.lineTo(x2, y2)
      ctx.stroke()
    }

    // Draw 2 longitudinal 6m beams (y = -1.5 and y = 1.5) with FEA heatmap segments
    for (const ym of [-1.5, 1.5]) {
      for (let i = 0; i < segments; i++) {
        const u0 = (i / segments) * 6 - 3
        const u1 = ((i + 1) / segments) * 6 - 3
        const d0 = computeBeamDeflectionMm(u0 + 3, effectiveInset)
        const d1 = computeBeamDeflectionMm(u1 + 3, effectiveInset)
        const norm = Math.abs((d0 + d1) * 0.5) / 24.63
        const [x1, y1] = project(u0, ym, zSkid - d0 * sagScale)
        const [x2, y2] = project(u1, ym, zSkid - d1 * sagScale)
        ctx.strokeStyle = mode === 'exploded' ? '#475569' : heatColor(norm)
        ctx.lineWidth = 7
        ctx.lineCap = 'round'
        ctx.beginPath()
        ctx.moveTo(x1, y1)
        ctx.lineTo(x2, y2)
        ctx.stroke()
      }
    }

    // Draw support piers / jacks at x = -3 + effectiveInset and x = 3 - effectiveInset
    if (mode !== 'exploded') {
      const sLeft = -3 + effectiveInset
      const sRight = 3 - effectiveInset
      for (const sx of [sLeft, sRight]) {
        for (const sy of [-1.5, 1.5]) {
          const [px1, py1] = project(sx, sy, zSkid)
          const [px2, py2] = project(sx, sy, -0.35)
          ctx.strokeStyle = '#38BDF8'
          ctx.lineWidth = 3
          ctx.beginPath()
          ctx.moveTo(px1, py1)
          ctx.lineTo(px2, py2)
          ctx.stroke()

          ctx.fillStyle = '#38BDF8'
          ctx.beginPath()
          ctx.arc(px1, py1, 4.5, 0, Math.PI * 2)
          ctx.fill()
        }
      }
    }

    // Layer 2: Corner Posts & Rigging Lugs
    const zPostsBase = zSkid + explodeFactor * 0.75
    const postHeight = 1.45
    const corners: [number, number][] = [
      [-3, -1.5],
      [3, -1.5],
      [3, 1.5],
      [-3, 1.5],
    ]
    for (const [cxm, cym] of corners) {
      const cornerSag = computeBeamDeflectionMm(cxm + 3, effectiveInset) * sagScale
      const [bx, by] = project(cxm, cym, zPostsBase - cornerSag)
      const [tx, ty] = project(cxm, cym, zPostsBase + postHeight - cornerSag)
      ctx.strokeStyle = '#94A3B8'
      ctx.lineWidth = 5
      ctx.beginPath()
      ctx.moveTo(bx, by)
      ctx.lineTo(tx, ty)
      ctx.stroke()

      // Corner casting node box
      ctx.fillStyle = '#F59E0B'
      ctx.beginPath()
      ctx.arc(tx, ty, 4, 0, Math.PI * 2)
      ctx.fill()
    }

    // Crane rigging slings in top-lift or inset-support mode
    if (mode !== 'exploded') {
      const [hookX, hookY] = project(0, 0, 3.1)
      ctx.fillStyle = '#FACC15'
      ctx.beginPath()
      ctx.arc(hookX, hookY, 6, 0, Math.PI * 2)
      ctx.fill()

      const slingX = mode === 'top-lift' ? 3.0 : 3.0 - effectiveInset
      const slingZ = mode === 'top-lift' ? zPostsBase + postHeight : zSkid
      for (const sx of [-slingX, slingX]) {
        for (const sy of [-1.5, 1.5]) {
          const attachSag = computeBeamDeflectionMm(sx + 3, effectiveInset) * sagScale
          const [ax, ay] = project(sx, sy, slingZ - attachSag)
          ctx.strokeStyle = 'rgba(250, 204, 21, 0.82)'
          ctx.lineWidth = 2
          ctx.setLineDash([5, 3])
          ctx.beginPath()
          ctx.moveTo(hookX, hookY)
          ctx.lineTo(ax, ay)
          ctx.stroke()
          ctx.setLineDash([])
        }
      }
    }

    // Layer 3: Reclaimed Wood Envelope Panels (shown in exploded mode or translucent in lift modes)
    const zWoodBase = zSkid + explodeFactor * 1.65
    const woodAlpha = mode === 'exploded' ? 0.88 : 0.18
    const drawQuad = (
      p1: [number, number, number],
      p2: [number, number, number],
      p3: [number, number, number],
      p4: [number, number, number],
      fill: string,
      stroke: string
    ) => {
      const [x1, y1] = project(...p1)
      const [x2, y2] = project(...p2)
      const [x3, y3] = project(...p3)
      const [x4, y4] = project(...p4)
      ctx.fillStyle = fill
      ctx.strokeStyle = stroke
      ctx.lineWidth = 1.5
      ctx.beginPath()
      ctx.moveTo(x1, y1)
      ctx.lineTo(x2, y2)
      ctx.lineTo(x3, y3)
      ctx.lineTo(x4, y4)
      ctx.closePath()
      ctx.fill()
      ctx.stroke()
    }

    // Back & Side Reclaimed Timber Walls
    drawQuad(
      [-2.9, -1.45, zWoodBase],
      [2.9, -1.45, zWoodBase],
      [2.9, -1.45, zWoodBase + 1.35],
      [-2.9, -1.45, zWoodBase + 1.35],
      `rgba(184, 115, 51, ${woodAlpha})`,
      `rgba(217, 119, 6, ${woodAlpha + 0.15})`
    )
    drawQuad(
      [-2.9, 1.45, zWoodBase],
      [-2.9, -1.45, zWoodBase],
      [-2.9, -1.45, zWoodBase + 1.35],
      [-2.9, 1.45, zWoodBase + 1.35],
      `rgba(161, 98, 42, ${woodAlpha})`,
      `rgba(217, 119, 6, ${woodAlpha + 0.15})`
    )

    // Layer 4: Roof & Glazing Cap
    const zRoofBase = zSkid + 1.45 + explodeFactor * 2.45
    const roofAlpha = mode === 'exploded' ? 0.9 : 0.22
    drawQuad(
      [-3.0, -1.5, zRoofBase],
      [3.0, -1.5, zRoofBase],
      [3.0, 0, zRoofBase + 0.35],
      [-3.0, 0, zRoofBase + 0.35],
      `rgba(30, 41, 59, ${roofAlpha})`,
      `rgba(148, 163, 184, ${roofAlpha + 0.2})`
    )
    drawQuad(
      [-3.0, 1.5, zRoofBase],
      [3.0, 1.5, zRoofBase],
      [3.0, 0, zRoofBase + 0.35],
      [-3.0, 0, zRoofBase + 0.35],
      `rgba(51, 65, 85, ${roofAlpha})`,
      `rgba(148, 163, 184, ${roofAlpha + 0.2})`
    )

    // Coordinate triad in bottom-left
    ctx.font = '11px ui-monospace, SFMono-Regular, Consolas, monospace'
    ctx.fillStyle = '#94A3B8'
    ctx.fillText('6000 × 3000 mm · Drag to rotate 3D · Scroll/buttons to zoom', 16, height - 14)
  }, [mode, effectiveInset, explodeFactor, yaw, pitch, zoom])

  return (
    <div
      style={{
        background: '#11151A',
        color: '#F1F5F9',
        borderRadius: '14px',
        border: '1px solid #262F3D',
        overflow: 'hidden',
        boxShadow: '0 16px 40px rgba(0,0,0,0.28)',
      }}
    >
      {/* Top Control Header */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          padding: '14px 18px',
          borderBottom: '1px solid #222B38',
          background: '#161B22',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <span style={{ fontWeight: 700, fontSize: '14px', letterSpacing: '0.03em' }}>
            3D STRUCTURAL & RIGGING LAB
          </span>
          <span
            style={{
              fontSize: '11px',
              padding: '2px 8px',
              borderRadius: '999px',
              background: 'rgba(217, 119, 6, 0.18)',
              color: '#FBBF24',
              border: '1px solid rgba(251, 191, 36, 0.35)',
              fontFamily: 'monospace',
            }}
          >
            [CONCEPTUAL · EULER-BERNOULLI 3000 KG REF]
          </span>
        </div>

        {/* Mode Switcher */}
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {(
            [
              { id: 'top-lift', label: 'Mode A: End / Top Corner Lift (a = 0 m)' },
              { id: 'inset-support', label: 'Mode B: Inset Supports (a = 1.2 m)' },
              { id: 'exploded', label: 'Mode C: 4-Layer Exploded BOM' },
            ] as const
          ).map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => setMode(item.id)}
              style={{
                padding: '6px 12px',
                fontSize: '12px',
                fontWeight: 600,
                borderRadius: '8px',
                cursor: 'pointer',
                border:
                  mode === item.id ? '1px solid #38BDF8' : '1px solid rgba(148,163,184,0.25)',
                background: mode === item.id ? 'rgba(56, 189, 248, 0.16)' : '#1E2530',
                color: mode === item.id ? '#38BDF8' : '#CBD5E1',
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main 3D Viewport + Telemetry Overlay */}
      <div style={{ position: 'relative', height: '420px', width: '100%' }}>
        <canvas
          ref={canvasRef}
          style={{ width: '100%', height: '100%', display: 'block', cursor: 'grab' }}
          onMouseDown={(e) => {
            dragRef.current = { active: true, x: e.clientX, y: e.clientY }
          }}
          onMouseMove={(e) => {
            if (!dragRef.current.active) return
            const dx = e.clientX - dragRef.current.x
            const dy = e.clientY - dragRef.current.y
            dragRef.current = { active: true, x: e.clientX, y: e.clientY }
            setYaw((prev) => prev + dx * 0.008)
            setPitch((prev) => Math.max(0.12, Math.min(1.15, prev + dy * 0.006)))
          }}
          onMouseUp={() => {
            dragRef.current.active = false
          }}
          onMouseLeave={() => {
            dragRef.current.active = false
          }}
        />

        {/* Deflection Readout Card (Top Right) */}
        <div
          style={{
            position: 'absolute',
            top: '14px',
            right: '14px',
            background: 'rgba(15, 23, 42, 0.88)',
            backdropFilter: 'blur(8px)',
            border: '1px solid rgba(148, 163, 184, 0.25)',
            borderRadius: '10px',
            padding: '12px 14px',
            maxWidth: '290px',
            fontSize: '12px',
          }}
        >
          <div style={{ color: '#94A3B8', marginBottom: '4px', fontFamily: 'monospace' }}>
            BEAM DEFLECTION COMPARISON
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '6px' }}>
            <span style={{ fontSize: '20px', fontWeight: 700, color: '#F43F5E' }}>24.63 mm</span>
            <span style={{ color: '#94A3B8' }}>vs</span>
            <span style={{ fontSize: '20px', fontWeight: 700, color: '#38BDF8' }}>
              {stats.maxAbsMm.toFixed(2)} mm
            </span>
          </div>
          <div style={{ color: '#CBD5E1', lineHeight: 1.4 }}>
            Support inset: <strong>{(effectiveInset * 1000).toFixed(0)} mm</strong> from ends ·
            Midspan sag: <strong>{stats.midspanMm.toFixed(2)} mm</strong>
          </div>
          {mode === 'inset-support' ? (
            <div style={{ marginTop: '10px' }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '11px',
                  color: '#38BDF8',
                  marginBottom: '4px',
                }}
              >
                Adjust Support Inset a = {insetMeters.toFixed(2)} m ({Math.round(insetMeters * 1000)}{' '}
                mm):
              </label>
              <input
                type="range"
                min={0}
                max={1.6}
                step={0.05}
                value={insetMeters}
                onChange={(e) => setInsetMeters(Number(e.target.value))}
                style={{ width: '100%' }}
              />
            </div>
          ) : null}
        </div>

        {/* Camera Zoom Controls (Bottom Right) */}
        <div
          style={{
            position: 'absolute',
            bottom: '14px',
            right: '14px',
            display: 'flex',
            gap: '6px',
          }}
        >
          <button
            type="button"
            onClick={() => setZoom((z) => Math.min(1.6, +(z + 0.15).toFixed(2)))}
            style={{
              padding: '5px 10px',
              borderRadius: '6px',
              border: '1px solid #334155',
              background: '#1E293B',
              color: '#E2E8F0',
              fontSize: '12px',
              cursor: 'pointer',
            }}
          >
            Zoom +
          </button>
          <button
            type="button"
            onClick={() => setZoom((z) => Math.max(0.65, +(z - 0.15).toFixed(2)))}
            style={{
              padding: '5px 10px',
              borderRadius: '6px',
              border: '1px solid #334155',
              background: '#1E293B',
              color: '#E2E8F0',
              fontSize: '12px',
              cursor: 'pointer',
            }}
          >
            Zoom −
          </button>
          <button
            type="button"
            onClick={() => {
              setYaw(-0.62)
              setPitch(0.42)
              setZoom(1.0)
            }}
            style={{
              padding: '5px 10px',
              borderRadius: '6px',
              border: '1px solid #334155',
              background: '#1E293B',
              color: '#E2E8F0',
              fontSize: '12px',
              cursor: 'pointer',
            }}
          >
            Reset View
          </button>
        </div>
      </div>

      {/* Bottom Interactive Layer Cards & Ask AI Trigger */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))',
          gap: '10px',
          padding: '14px 18px',
          background: '#161B22',
          borderTop: '1px solid #222B38',
        }}
      >
        {MINIHOUSE_BOM_LAYERS.map((item) => {
          const active = selectedLayer.id === item.id
          return (
            <div
              key={item.id}
              onClick={() => setSelectedLayer(item)}
              style={{
                padding: '10px 12px',
                borderRadius: '10px',
                border: active ? '1px solid #38BDF8' : '1px solid #262F3D',
                background: active ? 'rgba(56, 189, 248, 0.08)' : '#11151A',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: '6px',
              }}
            >
              <div>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    fontSize: '11px',
                    fontFamily: 'monospace',
                    color: '#94A3B8',
                  }}
                >
                  <span>
                    L{item.layer} · {item.id}
                  </span>
                  <span
                    style={{
                      padding: '1px 6px',
                      borderRadius: '4px',
                      background:
                        item.status === 'CALCULADO'
                          ? 'rgba(56, 189, 248, 0.2)'
                          : 'rgba(245, 158, 11, 0.2)',
                      color: item.status === 'CALCULADO' ? '#38BDF8' : '#FBBF24',
                    }}
                  >
                    [{item.status}]
                  </span>
                </div>
                <div style={{ fontWeight: 600, fontSize: '13px', marginTop: '4px' }}>
                  {item.name}
                </div>
                <div style={{ fontSize: '11px', color: '#94A3B8', marginTop: '2px' }}>
                  {item.dimensionsMm}
                </div>
              </div>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation()
                  onAskAi(item.prompt)
                }}
                style={{
                  marginTop: '6px',
                  padding: '5px 8px',
                  fontSize: '11px',
                  fontWeight: 600,
                  borderRadius: '6px',
                  border: '1px solid rgba(56, 189, 248, 0.4)',
                  background: 'rgba(56, 189, 248, 0.12)',
                  color: '#38BDF8',
                  cursor: 'pointer',
                  textAlign: 'left',
                }}
              >
                Ask Free AI about {item.id} →
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}
