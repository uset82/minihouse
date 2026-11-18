/** Only mirrored site pages have sibling language routes. The bilingual 404 links home. */
export function localePaths(pathname: string) {
  const section = pathname.replace(/^\/en(?=\/|$)/, '').replace(/\/+$/, '');
  if (section === '/personvern') return { nb: '/personvern/', en: '/en/personvern/' };
  if (section === '/historien') return { nb: '/historien/', en: '/en/historien/' };
  return { nb: '/', en: '/en/' };
}
