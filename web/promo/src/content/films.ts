/**
 * The concept film (DESIGN-GUIDE §6.15). films.json lists the web cuts that
 * scripts/cut_film.py makes from Carlos's walkthrough. The videos live in public/film/ and
 * the posters in src/assets/film/; both are media, so they stay out of git.
 */
import type { ImageMetadata } from 'astro';
import entries from './films.json';

export type FilmId = 'house' | 'living' | 'bath';

export type FilmStatus = 'approved' | 'pending' | 'stand-in';

type FilmEntry = {
  id: FilmId;
  file: string;
  poster: string;
  width: number;
  height: number;
  /** Optional sharper file for wide screens; same edit and aspect ratio. */
  wide?: { file: string; width: number; height: number };
  status: FilmStatus;
  source: string;
};

export type Film = FilmEntry & { src: string; srcWide?: string; posterImage: ImageMetadata };

const posters = import.meta.glob<{ default: ImageMetadata }>('../assets/film/*.{jpg,jpeg,png,webp}', {
  eager: true,
});

/** The film with its poster, or undefined when the media isn't on this machine. */
export function getFilm(id: FilmId): Film | undefined {
  const entry = (entries as FilmEntry[]).find((film) => film.id === id);
  const posterImage = entry ? posters[`../assets/film/${entry.poster}`]?.default : undefined;
  return entry && posterImage
    ? {
      ...entry,
      src: `/film/${entry.file}`,
      ...(entry.wide ? { srcWide: `/film/${entry.wide.file}` } : {}),
      posterImage,
    }
    : undefined;
}
