import { contentShape, readJson, validateImages, validateShape } from './content-contract.mjs';

const errors = [];
const nb = readJson('src/content/nb.json');
const en = readJson('src/content/en.json');
const images = readJson('src/content/images.json');

validateShape(nb, contentShape, 'nb', errors);
validateShape(en, contentShape, 'en', errors);
validateImages(images, errors);

if (errors.length > 0) {
  console.error(`content check failed (${errors.length})`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log('content check passed');
