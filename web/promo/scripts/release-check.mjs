import { findTodos, readJson, validateImages, validateShape, contentShape } from './content-contract.mjs';

const errors = [];
const nb = readJson('src/content/nb.json');
const en = readJson('src/content/en.json');
const images = readJson('src/content/images.json');

validateShape(nb, contentShape, 'nb', errors);
validateShape(en, contentShape, 'en', errors);
validateImages(images, errors);

const todos = [];
findTodos(nb, 'nb', todos);
findTodos(en, 'en', todos);
findTodos(images, 'images', todos);

for (const [index, image] of images.entries()) {
  if (image.status !== 'approved') {
    errors.push(`images[${index}] (${image.id}) status is ${image.status}; a release needs approved`);
  }
  if (typeof image.file !== 'string' || image.file.length === 0) {
    errors.push(`images[${index}] (${image.id}) has no file`);
  }
}

if (todos.length > 0) {
  errors.push(`${todos.length} TODO value(s), first: ${todos.slice(0, 8).join(', ')}`);
}

if (errors.length > 0) {
  console.error(`release check failed (${errors.length})`);
  for (const error of errors.slice(0, 30)) console.error(`- ${error}`);
  if (errors.length > 30) console.error(`- … ${errors.length - 30} more`);
  process.exit(1);
}

console.log('release check passed');
