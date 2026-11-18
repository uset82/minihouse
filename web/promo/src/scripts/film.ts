/*
 * The concept film (DESIGN-GUIDE §6.15): every film on the page shares one state.
 * - It plays by itself, without sound, unless the visitor prefers reduced motion, has Data
 *   Saver on, or paused it earlier in this tab. Then the still frame shows.
 * - Any «Pause filmen» button pauses every film; the choice lasts for the tab (sessionStorage,
 *   no cookie), across reloads and other pages.
 * - Nothing loads before the window's load event, a film only loads when it comes near the
 *   screen, and films off screen or in a hidden tab are paused.
 */
const KEY = 'minihouse-film';

const videos = Array.from(document.querySelectorAll<HTMLVideoElement>('video[data-film-src]'));
const toggles = Array.from(document.querySelectorAll<HTMLButtonElement>('[data-film-toggle]'));

const stored = (): string | null => {
  try {
    return sessionStorage.getItem(KEY);
  } catch {
    return null;
  }
};

const store = (value: 'playing' | 'paused') => {
  try {
    sessionStorage.setItem(KEY, value);
  } catch {
    // Storage is off: the choice lasts until the page reloads.
  }
};

if (videos.length > 0) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const wideScreen = window.matchMedia('(min-width: 64rem)');
  const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
  const choice = stored();
  let playing = choice === 'playing' || (choice === null && !reduceMotion.matches && connection?.saveData !== true);
  const near = new Set<HTMLVideoElement>();

  const label = () => {
    for (const toggle of toggles) {
      toggle.textContent = (playing ? toggle.dataset.pause : toggle.dataset.play) ?? '';
    }
  };

  const update = () => {
    for (const video of videos) {
      const show = playing && near.has(video) && document.visibilityState === 'visible';
      if (show) {
        // Choose once, when the film loads: the sharper hero cut from 64rem up.
        if (!video.getAttribute('src')) {
          video.src = (wideScreen.matches && video.dataset.filmSrcWide
            ? video.dataset.filmSrcWide
            : video.dataset.filmSrc) ?? '';
        }
        video.play().then(
          () => video.classList.add('is-playing'),
          (error: unknown) => {
            // Autoplay refused, or the film can't play here at all: keep the still and
            // offer «Spill av filmen». An AbortError only means a pause came first.
            if (error instanceof DOMException && error.name !== 'AbortError' && playing) {
              playing = false;
              update();
            }
          },
        );
      } else if (!video.paused) {
        video.pause();
      }
    }
    label();
  };

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const video = entry.target as HTMLVideoElement;
        if (entry.isIntersecting) near.add(video);
        else near.delete(video);
      }
      update();
    },
    { rootMargin: '25% 0px' },
  );

  const start = () => videos.forEach((video) => observer.observe(video));
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start, { once: true });

  for (const toggle of toggles) {
    toggle.addEventListener('click', () => {
      playing = !playing;
      store(playing ? 'playing' : 'paused');
      update();
    });
  }

  document.addEventListener('visibilitychange', update);
  reduceMotion.addEventListener('change', () => {
    if (reduceMotion.matches && stored() !== 'playing') {
      playing = false;
      update();
    }
  });

  label();
}
