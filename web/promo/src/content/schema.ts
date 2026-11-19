/**
 * Content contract for nb.json and en.json (agents/README.md §4.1).
 * Cursor owns this file. DeepSeek owns the JSON values.
 * A missing key fails `npm run check`.
 */

export type Passport = {
  material: string;
  origin: string;
  previousUse: string;
  usedFor: string;
  treatment: string;
  status: string;
};

export type Content = {
  meta: {
    title: string;
    description: string;
    ogAlt: string;
  };
  nav: {
    skip: string;
    house: string;
    materials: string;
    moving: string;
    questions: string;
    story: string;
    cta: string;
    menu: string;
    close: string;
    language: string;
  };
  hero: {
    title: string;
    lead: string;
    cta: string;
    gallery: string;
    caption: string;
  };
  facts: {
    items: Array<{ label: string; value: string }>;
  };
  gallery: {
    title: string;
    count: string;
    prev: string;
    next: string;
    close: string;
    note: string;
  };
  build: {
    title: string;
    lead: string;
    tabExterior: string;
    tabStructure: string;
    exterior: string;
    structure: string;
  };
  materials: {
    title: string;
    lead: string;
    passportTitle: string;
    rows: Passport;
    items: Array<{
      id: string;
      name: string;
      lead: string;
      passport: Passport;
    }>;
  };
  living: {
    title: string;
    lead: string;
    rooms: Array<{ id: string; title: string; body: string }>;
  };
  /** The concept film (DESIGN-GUIDE §6.15): caption, the shared play/pause words, and what each cut shows. */
  film: {
    caption: string;
    play: string;
    pause: string;
    alt: string;
    livingAlt: string;
    bathAlt: string;
  };
  journey: {
    title: string;
    steps: Array<{ title: string; body: string }>;
  };
  status: {
    title: string;
    body: string;
    phases: Array<{ name: string; state: string }>;
  };
  faq: {
    title: string;
    items: Array<{ q: string; a: string }>;
  };
  interest: {
    title: string;
    lead: string;
    fields: {
      email: string;
      /** Label for the name field. The field itself is optional. */
      name: string;
      /** The "(valgfritt)" marker, used on the name field. */
      optional: string;
    };
    consent: string;
    submit: string;
    success: string;
    errors: {
      required: string;
      email: string;
      network: string;
    };
  };
  footer: {
    contact: string;
    privacy: string;
    pro: string;
    docs: string;
    lab: string;
    imagesNote: string;
  };
  privacy: {
    title: string;
    body: string;
  };
  notFound: {
    title: string;
    body: string;
    home: string;
  };
  story: {
    meta: { title: string; description: string };
    title: string;
    byline: string;
    lead: string;
    intro: string[];
    reference: { label: string; link: string; href: string };
    noticed: string[];
    question: string;
    questionFollow: string;
    origin: string;
    sections: Array<{ title: string; paragraphs: string[] }>;
    closing: string;
    motto: string[];
    cta: string;
    teaser: { title: string; body: string; link: string };
    film: { alt: string; caption: string };
  };
};
