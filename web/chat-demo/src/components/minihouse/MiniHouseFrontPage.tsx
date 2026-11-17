import { useState } from 'react'
import { openSettings } from '../settings/settingsDialogState.js'
import { setDraftText } from '../../services/chat/drafts.js'
import { useChatStore } from '../../services/chat/store.js'
import { useSettings } from '../../services/settings.js'
import { MINIHOUSE_BOM_LAYERS, MiniHouse3DSimulator } from './MiniHouse3DSimulator.js'

export type WorkspaceViewMode = 'overview' | 'split' | 'chat'

const CONCEPT_CARDS = [
  {
    id: 'concept-1',
    title: 'Concept 1 · Nordic Craft & Steel Documentary Hero',
    badge: '[CONCEPTUAL · REV 0.1]',
    description:
      'Editorial documentary presentation of the 6000 × 3000 mm transportable cabin (height TBD with gable roof) on adjustable piers, pairing a steel primary frame (grade TBD) with reclaimed Nordic timber (batch documentation pending).',
  },
  {
    id: 'concept-2',
    title: 'Concept 2 · Interactive 3D Lifting & FEA Deflection Lab',
    badge: '[CONCEPTUAL · 3 t REFERENCE BEAM]',
    description:
      'Dark-mode structural twin comparing Mode A (Top-Corner Lift, 24.63 mm deflection) vs. Mode B (1.2 m Inset Supports, 1.49 mm deflection) — hypothetical 3 t reference beam from the research report, NOT the module — alongside the OpenRouter Free AI Assistant.',
  },
  {
    id: 'concept-3',
    title: 'Concept 3 · 4-Layer Exploded BOM & Material Passport',
    badge: '[TRACEABLE BOM]',
    description:
      'Exploded axonometric view separating the steel skid, corner nodes, reclaimed barn timber panels, and standing-seam roof with component IDs and verification badges.',
  },
] as const

const PHASE_ROADMAP = [
  {
    phase: 'Phase 0 · Context & Harness',
    status: 'COMPLETED',
    items: [
      '6 specialist agents & 6 canonical skills defined in .agents/',
      'OpenRouter Free SDK (@openrouter/sdk) integrated in web/chat-demo & web/deepseek-harness',
      'Zero-cost model guardrails enforced (openrouter/free & :free variants)',
    ],
  },
  {
    phase: 'Phase 1 · Data & Feasibility',
    status: 'ACTIVE',
    items: [
      'Confirm destination in Norway, transport route width/height limits, and crane reach',
      'Complete reference floorplan, elevations, openings, and component mass inventory',
      'Define transport, rigging, and support conditions with structural & lifting specialists',
    ],
  },
  {
    phase: 'Phase 2 · Structural Model & BIM',
    status: 'PENDING',
    items: [
      'Verify Robot Structural Analysis ↔ Advance Steel (SMLX) test file transfer',
      'Compute real center of gravity, reactions, torsion, and corner node forces',
      'Compare top-corner lift vs. base lift and select prototype variant',
    ],
  },
  {
    phase: 'Phase 3 · Prototype & Lifting Tests',
    status: 'PENDING',
    items: [
      'Detail pilot corner joint and issue workshop drawings (mm)',
      'Execute instrumented crane-lift and road-transport tests and compare with solver',
    ],
  },
] as const

export const TopNavigationHeader = ({
  viewMode,
  setViewMode,
  drawerOpen,
  setDrawerOpen,
}: {
  viewMode: WorkspaceViewMode
  setViewMode: (mode: WorkspaceViewMode) => void
  drawerOpen: boolean
  setDrawerOpen: (open: boolean) => void
}) => {
  const selectedModel = useSettings((s) => s.selectedModel)
  const apiKey = useSettings((s) => s.apiKey)

  return (
    <header
      style={{
        height: '54px',
        padding: '0 20px',
        background: '#161B22',
        color: '#F8FAFC',
        borderBottom: '1px solid #262F3D',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '12px',
        flexShrink: 0,
        zIndex: 40,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontWeight: 800, fontSize: '15px', letterSpacing: '0.04em' }}>
          MINIHOUSE <span style={{ color: '#D97706' }}>6×3M</span>
        </span>
        <span
          style={{
            fontSize: '11px',
            padding: '2px 8px',
            borderRadius: '999px',
            background: 'rgba(217, 119, 6, 0.16)',
            color: '#FBBF24',
            border: '1px solid rgba(251, 191, 36, 0.3)',
            fontFamily: 'monospace',
          }}
        >
          [CONCEPTUAL · REV 0.1]
        </span>
      </div>

      {/* View Switcher */}
      <nav aria-label="Workspace View Mode" style={{ display: 'flex', gap: '6px' }}>
        {(
          [
            { id: 'overview', label: '1. Documentary + 3D Lab' },
            { id: 'split', label: '2. 3D + AI Split View' },
            { id: 'chat', label: '3. Full AI Chat' },
          ] as const
        ).map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setViewMode(tab.id)}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              border:
                viewMode === tab.id ? '1px solid #D97706' : '1px solid rgba(148,163,184,0.22)',
              background: viewMode === tab.id ? '#D97706' : 'transparent',
              color: viewMode === tab.id ? '#11151A' : '#E2E8F0',
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Right Status & Settings / AI Drawer Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <button
          type="button"
          onClick={() => openSettings(apiKey ? 'general' : 'data')}
          title="Configure Free OpenRouter Model & API Key"
          style={{
            padding: '5px 10px',
            borderRadius: '8px',
            fontSize: '11px',
            fontFamily: 'monospace',
            border: '1px solid #334155',
            background: '#1E293B',
            color: '#38BDF8',
            cursor: 'pointer',
          }}
        >
          Model: {selectedModel} ⚙
        </button>
        {viewMode === 'overview' ? (
          <button
            type="button"
            onClick={() => setDrawerOpen(!drawerOpen)}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: 700,
              border: '1px solid #38BDF8',
              background: drawerOpen ? '#38BDF8' : 'rgba(56, 189, 248, 0.14)',
              color: drawerOpen ? '#0F172A' : '#38BDF8',
              cursor: 'pointer',
            }}
          >
            {drawerOpen ? 'Hide AI Drawer' : 'Ask Free AI 💬'}
          </button>
        ) : null}
      </div>
    </header>
  )
}

export const MiniHouseDocumentaryContent = ({
  onAskAi,
}: {
  onAskAi: (prompt: string) => void
}) => {
  const [selectedConcept, setSelectedConcept] = useState(0)

  return (
    <div
      style={{
        flex: 1,
        overflowY: 'auto',
        background: '#F5F2EB',
        color: '#1E2328',
        paddingBottom: '64px',
      }}
    >
      {/* SECTION 1: NORDIC HERO */}
      <section
        style={{
          maxWidth: '1240px',
          margin: '0 auto',
          padding: '36px 24px 28px',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
          gap: '28px',
          alignItems: 'center',
        }}
      >
        <div>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '4px 10px',
              borderRadius: '999px',
              background: '#E6DFD3',
              color: '#78350F',
              fontSize: '11px',
              fontWeight: 700,
              fontFamily: 'monospace',
              marginBottom: '14px',
            }}
          >
            <span>NORWAY REFERENCE · TEK17 / NS-EN 1993</span>
            <span>·</span>
            <span>[CONCEPTUAL · REV 0.1]</span>
          </div>

          <h1
            style={{
              fontSize: 'clamp(28px, 3.5vw, 42px)',
              lineHeight: 1.12,
              fontWeight: 800,
              margin: '0 0 14px',
              color: '#14181D',
            }}
          >
            MINIHOUSE 6×3M — STEEL CHASSIS & RECLAIMED WOOD
          </h1>

          <p
            style={{
              fontSize: '15px',
              lineHeight: 1.6,
              color: '#334155',
              margin: '0 0 20px',
            }}
          >
            A transportable <strong>6000 × 3000 mm</strong> modular cabin designed to be lifted by
            crane, transported by flatbed truck, and placed on site without permanent deformation of
            the primary steel frame, corner nodes, or door/window openings (engineering in progress).
          </p>

          {/* Key Dimension & Traceability Pills */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '10px',
              marginBottom: '20px',
            }}
          >
            <div
              style={{
                background: '#FFFFFF',
                padding: '10px 12px',
                borderRadius: '10px',
                border: '1px solid #DFD9CE',
              }}
            >
              <div style={{ fontSize: '11px', color: '#64748B', fontFamily: 'monospace' }}>
                FOOTPRINT
              </div>
              <div style={{ fontSize: '15px', fontWeight: 700, marginTop: '2px' }}>
                6000 × 3000 mm
              </div>
              <div style={{ fontSize: '10px', color: '#D97706', fontFamily: 'monospace' }}>
                [CONCEPTUAL]
              </div>
            </div>
            <div
              style={{
                background: '#FFFFFF',
                padding: '10px 12px',
                borderRadius: '10px',
                border: '1px solid #DFD9CE',
              }}
            >
              <div style={{ fontSize: '11px', color: '#64748B', fontFamily: 'monospace' }}>
                INSET DEFLECTION · 3 t REFERENCE BEAM
              </div>
              <div style={{ fontSize: '15px', fontWeight: 700, marginTop: '2px' }}>
                1.49 mm (a=1.2m)
              </div>
              <div style={{ fontSize: '10px', color: '#D97706', fontFamily: 'monospace' }}>
                [CONCEPTUAL · HYPOTHETICAL EXAMPLE, NOT MODULE]
              </div>
            </div>
            <div
              style={{
                background: '#FFFFFF',
                padding: '10px 12px',
                borderRadius: '10px',
                border: '1px solid #DFD9CE',
              }}
            >
              <div style={{ fontSize: '11px', color: '#64748B', fontFamily: 'monospace' }}>
                AI BACKEND
              </div>
              <div style={{ fontSize: '15px', fontWeight: 700, marginTop: '2px' }}>
                OpenRouter Free
              </div>
              <div style={{ fontSize: '10px', color: '#16A34A', fontFamily: 'monospace' }}>
                [@openrouter/sdk · $0]
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            <button
              type="button"
              onClick={() =>
                onAskAi(
                  'Compare top-corner lifting vs. base lifting with 1.2 m inset supports for the 6×3 m MiniHouse steel chassis, including how openings are protected from racking.'
                )
              }
              style={{
                padding: '10px 16px',
                borderRadius: '9px',
                border: 'none',
                background: '#1E2328',
                color: '#F5F2EB',
                fontWeight: 700,
                fontSize: '13px',
                cursor: 'pointer',
              }}
            >
              Ask AI: Top Lift vs. Base Lift →
            </button>
            <button
              type="button"
              onClick={() =>
                onAskAi(
                  'Generate a Mermaid diagram of the MiniHouse load path during crane lifting and explain the verification statuses [CONCEPTUAL], [CALCULADO], [ENSAYADO], and [LIBERADO].'
                )
              }
              style={{
                padding: '10px 16px',
                borderRadius: '9px',
                border: '1px solid #B87333',
                background: 'rgba(184, 115, 51, 0.12)',
                color: '#78350F',
                fontWeight: 700,
                fontSize: '13px',
                cursor: 'pointer',
              }}
            >
              Ask AI: Load Path & Mermaid Diagram →
            </button>
          </div>
        </div>

        {/* Hero Concept Visual Switcher */}
        <div
          style={{
            background: '#FFFFFF',
            borderRadius: '14px',
            border: '1px solid #DFD9CE',
            overflow: 'hidden',
            boxShadow: '0 14px 34px rgba(20, 24, 29, 0.08)',
          }}
        >
          <div
            style={{
              width: '100%',
              minHeight: '120px',
              display: 'flex',
              alignItems: 'center',
              padding: '20px 16px',
              background: '#E8E4DC',
              color: '#1E2328',
              fontSize: '14px',
              lineHeight: 1.5,
            }}
          >
            Concept pictures withdrawn. They showed a flat-roofed container and are archived, not the MiniHouse design.
          </div>
          <div style={{ padding: '14px 16px' }}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '8px',
                marginBottom: '6px',
              }}
            >
              <strong style={{ fontSize: '14px' }}>{CONCEPT_CARDS[selectedConcept].title}</strong>
              <span
                style={{
                  fontSize: '11px',
                  fontFamily: 'monospace',
                  color: '#B87333',
                  fontWeight: 700,
                }}
              >
                {CONCEPT_CARDS[selectedConcept].badge}
              </span>
            </div>
            <p style={{ fontSize: '12px', color: '#475569', margin: '0 0 12px', lineHeight: 1.5 }}>
              {CONCEPT_CARDS[selectedConcept].description}
            </p>
            <div style={{ display: 'flex', gap: '6px' }}>
              {CONCEPT_CARDS.map((card, idx) => (
                <button
                  key={card.id}
                  type="button"
                  onClick={() => setSelectedConcept(idx)}
                  style={{
                    flex: 1,
                    padding: '6px 8px',
                    fontSize: '11px',
                    fontWeight: 600,
                    borderRadius: '6px',
                    cursor: 'pointer',
                    border:
                      selectedConcept === idx ? '1px solid #1E2328' : '1px solid #E2E8F0',
                    background: selectedConcept === idx ? '#1E2328' : '#F8FAFC',
                    color: selectedConcept === idx ? '#FFFFFF' : '#475569',
                  }}
                >
                  Concept {idx + 1}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 2: INTERACTIVE 3D CRANE-LIFTING & EXPLODED ASSEMBLY SIMULATOR */}
      <section style={{ maxWidth: '1240px', margin: '0 auto', padding: '12px 24px 28px' }}>
        <MiniHouse3DSimulator onAskAi={onAskAi} />
      </section>

      {/* SECTION 3: TRACEABLE BOM & PHASE ROADMAP */}
      <section
        style={{
          maxWidth: '1240px',
          margin: '0 auto',
          padding: '8px 24px',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
          gap: '24px',
        }}
      >
        {/* Traceable Bill of Materials */}
        <div
          style={{
            background: '#FFFFFF',
            borderRadius: '14px',
            border: '1px solid #DFD9CE',
            padding: '20px',
          }}
        >
          <h2 style={{ fontSize: '17px', fontWeight: 800, margin: '0 0 6px' }}>
            Traceable Assembly & Material Passport
          </h2>
          <p style={{ fontSize: '12px', color: '#64748B', margin: '0 0 14px' }}>
            Every published figure retains its component ID, material origin, and verification state
            per <code>rules.md</code>.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {MINIHOUSE_BOM_LAYERS.map((layer) => (
              <div
                key={layer.id}
                style={{
                  padding: '10px 12px',
                  borderRadius: '8px',
                  background: '#F8F6F1',
                  border: '1px solid #E5E0D5',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: '12px',
                }}
              >
                <div>
                  <div style={{ fontSize: '13px', fontWeight: 700 }}>
                    {layer.id} · {layer.name}
                  </div>
                  <div style={{ fontSize: '12px', color: '#475569', marginTop: '2px' }}>
                    {layer.material} · <code>{layer.dimensionsMm}</code>
                  </div>
                </div>
                <span
                  style={{
                    fontSize: '11px',
                    fontFamily: 'monospace',
                    fontWeight: 700,
                    padding: '3px 8px',
                    borderRadius: '6px',
                    background: layer.status === 'CALCULADO' ? '#E0F2FE' : '#FEF3C7',
                    color: layer.status === 'CALCULADO' ? '#0369A1' : '#B45309',
                    flexShrink: 0,
                  }}
                >
                  [{layer.status}]
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Project Phases */}
        <div
          style={{
            background: '#FFFFFF',
            borderRadius: '14px',
            border: '1px solid #DFD9CE',
            padding: '20px',
          }}
        >
          <h2 style={{ fontSize: '17px', fontWeight: 800, margin: '0 0 6px' }}>
            Sequential Engineering Plan (PROJECT.md)
          </h2>
          <p style={{ fontSize: '12px', color: '#64748B', margin: '0 0 14px' }}>
            Live progress across structural analysis, CAD/BIM coordination, lifting validation, and
            web documentation.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {PHASE_ROADMAP.map((p) => (
              <div
                key={p.phase}
                style={{
                  padding: '10px 12px',
                  borderRadius: '8px',
                  background: '#F8F6F1',
                  border: '1px solid #E5E0D5',
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '4px',
                  }}
                >
                  <strong style={{ fontSize: '13px' }}>{p.phase}</strong>
                  <span
                    style={{
                      fontSize: '10px',
                      fontFamily: 'monospace',
                      fontWeight: 700,
                      padding: '2px 7px',
                      borderRadius: '999px',
                      background:
                        p.status === 'COMPLETED'
                          ? '#DCFCE7'
                          : p.status === 'ACTIVE'
                            ? '#FEF3C7'
                            : '#F1F5F9',
                      color:
                        p.status === 'COMPLETED'
                          ? '#15803D'
                          : p.status === 'ACTIVE'
                            ? '#B45309'
                            : '#64748B',
                    }}
                  >
                    {p.status}
                  </span>
                </div>
                <ul
                  style={{
                    margin: 0,
                    paddingLeft: '16px',
                    fontSize: '12px',
                    color: '#475569',
                    lineHeight: 1.5,
                  }}
                >
                  {p.items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

/**
 * Helper to prefill the active chat session's draft input with a technical prompt from the 3D simulator or hero buttons.
 */
export const prefillAiQuestion = (prompt: string) => {
  const activeId = useChatStore.getState().activeId
  setDraftText(activeId, prompt)
}
