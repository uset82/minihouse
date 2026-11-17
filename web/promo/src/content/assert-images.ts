import imagesJson from './images.json';
import {
  imageIds,
  type ImageId,
  type ImageKind,
  type ImageStatus,
  type PromoImage,
} from './images';

const kinds = new Set<ImageKind>(['render', 'photo', 'texture']);
const statuses = new Set<ImageStatus>(['approved', 'pending', 'stand-in']);
const knownIds = new Set<string>(imageIds);

function readString(value: unknown, path: string): string {
  if (typeof value !== 'string') throw new Error(`${path} must be a string`);
  return value;
}

function readNullableString(value: unknown, path: string): string | null {
  if (value === null) return null;
  return readString(value, path);
}

function readPair(value: unknown, path: string): { nb: string; en: string } {
  if (!value || typeof value !== 'object') throw new Error(`${path} must be an object`);
  const pair = value as { nb?: unknown; en?: unknown };
  return {
    nb: readString(pair.nb, `${path}.nb`),
    en: readString(pair.en, `${path}.en`),
  };
}

function parseImages(value: unknown): PromoImage[] {
  if (!Array.isArray(value)) throw new Error('images.json must be an array');
  const seen = new Set<string>();
  const images = value.map((entry, index) => {
    const path = `images[${index}]`;
    if (!entry || typeof entry !== 'object') throw new Error(`${path} must be an object`);
    const image = entry as Record<string, unknown>;
    const id = readString(image.id, `${path}.id`);
    if (!knownIds.has(id)) throw new Error(`${path}.id is unknown`);
    if (seen.has(id)) throw new Error(`${path}.id is duplicated`);
    seen.add(id);
    const kind = readString(image.kind, `${path}.kind`);
    const status = readString(image.status, `${path}.status`);
    if (!kinds.has(kind as ImageKind)) throw new Error(`${path}.kind is invalid`);
    if (!statuses.has(status as ImageStatus)) throw new Error(`${path}.status is invalid`);
    return {
      id: id as ImageId,
      file: readNullableString(image.file, `${path}.file`),
      kind: kind as ImageKind,
      status: status as ImageStatus,
      alt: readPair(image.alt, `${path}.alt`),
      caption: readPair(image.caption, `${path}.caption`),
      source: readNullableString(image.source, `${path}.source`),
      focal: readString(image.focal, `${path}.focal`),
    };
  });
  for (const id of imageIds) {
    if (!seen.has(id)) throw new Error(`images.json is missing id ${id}`);
  }
  return images;
}

export const images: PromoImage[] = parseImages(imagesJson);
