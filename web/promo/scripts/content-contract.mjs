import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

const passport = {
  material: '',
  origin: '',
  previousUse: '',
  usedFor: '',
  treatment: '',
  status: '',
};

/** Key tree for nb.json and en.json. Empty string = string, array = that item shape. */
export const contentShape = {
  meta: { title: '', description: '', ogAlt: '' },
  nav: {
    skip: '',
    house: '',
    materials: '',
    moving: '',
    questions: '',
    cta: '',
    menu: '',
    close: '',
    language: '',
  },
  hero: { title: '', lead: '', cta: '', gallery: '', caption: '' },
  facts: { items: [{ label: '', value: '' }] },
  gallery: { title: '', count: '', prev: '', next: '', close: '' },
  build: {
    title: '',
    lead: '',
    tabExterior: '',
    tabStructure: '',
    exterior: '',
    structure: '',
  },
  materials: {
    title: '',
    lead: '',
    passportTitle: '',
    rows: passport,
    items: [{ id: '', name: '', lead: '', passport }],
  },
  living: {
    title: '',
    lead: '',
    rooms: [{ id: '', title: '', body: '' }],
  },
  journey: { title: '', steps: [{ title: '', body: '' }] },
  status: { title: '', body: '', phases: [{ name: '', state: '' }] },
  faq: { title: '', items: [{ q: '', a: '' }] },
  interest: {
    title: '',
    lead: '',
    fields: {
      email: '',
      name: '',
      optional: '',
    },
    consent: '',
    submit: '',
    success: '',
    errors: { required: '', email: '', network: '' },
  },
  footer: {
    contact: '',
    privacy: '',
    pro: '',
    docs: '',
    lab: '',
    imagesNote: '',
  },
  privacy: { title: '', body: '' },
  notFound: { title: '', body: '', home: '' },
};

const imageKinds = new Set(['render', 'photo', 'texture']);
const imageStatuses = new Set(['approved', 'pending', 'stand-in']);

export function readJson(relativePath) {
  return JSON.parse(readFileSync(join(root, relativePath), 'utf8'));
}

export function readImageIds() {
  const source = readFileSync(join(root, 'src/content/images.ts'), 'utf8');
  const block = source.match(/export const imageIds = \[([\s\S]*?)\] as const/);
  if (!block) {
    throw new Error('Could not read imageIds from src/content/images.ts');
  }
  return [...block[1].matchAll(/'([^']+)'/g)].map((match) => match[1]);
}

export function validateShape(actual, shape, path, errors) {
  if (typeof shape === 'string') {
    if (typeof actual !== 'string') errors.push(`${path} must be a string`);
    return;
  }
  if (Array.isArray(shape)) {
    if (!Array.isArray(actual)) {
      errors.push(`${path} must be an array`);
      return;
    }
    const itemShape = shape[0];
    actual.forEach((item, index) => {
      validateShape(item, itemShape, `${path}[${index}]`, errors);
    });
    return;
  }
  if (!actual || typeof actual !== 'object' || Array.isArray(actual)) {
    errors.push(`${path} must be an object`);
    return;
  }
  for (const key of Object.keys(shape)) {
    const next = path ? `${path}.${key}` : key;
    if (!Object.hasOwn(actual, key)) {
      errors.push(`${next} is missing`);
      continue;
    }
    validateShape(actual[key], shape[key], next, errors);
  }
}

export function validateImages(images, errors) {
  if (!Array.isArray(images)) {
    errors.push('images.json must be an array');
    return;
  }
  const expected = readImageIds();
  const seen = new Set();
  images.forEach((image, index) => {
    const path = `images[${index}]`;
    if (!image || typeof image !== 'object') {
      errors.push(`${path} must be an object`);
      return;
    }
    for (const field of ['id', 'file', 'kind', 'status', 'alt', 'caption', 'source', 'focal']) {
      if (!Object.hasOwn(image, field)) errors.push(`${path}.${field} is missing`);
    }
    if (image.file !== null && typeof image.file !== 'string') {
      errors.push(`${path}.file must be a string or null`);
    }
    if (!imageKinds.has(image.kind)) errors.push(`${path}.kind is invalid`);
    if (!imageStatuses.has(image.status)) errors.push(`${path}.status is invalid`);
    if (typeof image.alt?.nb !== 'string' || typeof image.alt?.en !== 'string') {
      errors.push(`${path}.alt.nb and alt.en must be strings`);
    }
    if (typeof image.caption?.nb !== 'string' || typeof image.caption?.en !== 'string') {
      errors.push(`${path}.caption.nb and caption.en must be strings`);
    }
    if (image.source !== null && typeof image.source !== 'string') {
      errors.push(`${path}.source must be a string or null`);
    }
    if (typeof image.focal !== 'string') errors.push(`${path}.focal must be a string`);
    if (typeof image.id === 'string') {
      if (seen.has(image.id)) errors.push(`${path}.id is duplicated`);
      seen.add(image.id);
    }
  });
  for (const id of expected) {
    if (!seen.has(id)) errors.push(`images.json is missing id ${id}`);
  }
  for (const id of seen) {
    if (!expected.includes(id)) errors.push(`images.json has unknown id ${id}`);
  }
}

export function findTodos(value, path, hits) {
  if (value === 'TODO') {
    hits.push(path);
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => findTodos(item, `${path}[${index}]`, hits));
    return;
  }
  if (value && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      findTodos(child, path ? `${path}.${key}` : key, hits);
    }
  }
}
