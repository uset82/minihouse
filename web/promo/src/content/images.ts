/**
 * Image contract (agents/README.md §4.2).
 * Cursor owns this file. Antigravity owns images.json and src/assets/images/ after handover.
 * Keep this id list in sync with scripts/check-content.mjs, which reads it.
 */

export const imageIds = [
  'hero-slope',
  'meadow-wide',
  'exploded',
  'living',
  'kitchen',
  'bench',
  'storage',
  'bath-shower',
  'bath-vanity',
  'bath-window',
  'bath-doorway',
  'journey-workshop',
  'journey-truck',
  'journey-plot',
  'texture-malmfuru',
  'texture-eik',
  'texture-kobber',
  'texture-stal',
  'og-image',
] as const;

export type ImageId = (typeof imageIds)[number];

export type ImageKind = 'render' | 'photo' | 'texture';

export type ImageStatus = 'approved' | 'pending' | 'stand-in';

export type PromoImage = {
  id: ImageId;
  file: string | null;
  kind: ImageKind;
  status: ImageStatus;
  alt: { nb: string; en: string };
  caption: { nb: string; en: string };
  source: string | null;
  focal: string;
};
