import { describe, expect, it } from 'vitest'
import {
  computeBeamDeflectionMm,
  computePeakDeflectionMm,
  MINIHOUSE_BOM_LAYERS,
} from './MiniHouse3DSimulator.js'

describe('MiniHouse3DSimulator Euler-Bernoulli verification', () => {
  it('computes 24.63 mm midspan deflection for end supports (a = 0 m) matching the structural report', () => {
    const midspan = computeBeamDeflectionMm(3.0, 0.0)
    expect(midspan).toBeCloseTo(24.63, 1)
  })

  it('reduces peak deflection to ~1.49 mm when supports are inset by a = 1.2 m from ends', () => {
    const stats = computePeakDeflectionMm(1.2)
    expect(stats.maxAbsMm).toBeCloseTo(1.49, 1)
  })

  it('maintains explicit verification status tags on all 4 BOM layers', () => {
    expect(MINIHOUSE_BOM_LAYERS).toHaveLength(4)
    for (const item of MINIHOUSE_BOM_LAYERS) {
      expect(['CONCEPTUAL', 'CALCULADO', 'ENSAYADO', 'LIBERADO']).toContain(item.status)
    }
  })
})
