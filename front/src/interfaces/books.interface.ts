export interface Book {
  authors: {
    birth_year: number;
    death_year: number;
    name: string;
  }[];
  bookshelves: any[];
  copyright: boolean;
  download_count: number;
  formats: {
    "application/epub+zip": string;
    "application/octet-stream": string;
    "application/rdf+xml": string;
    "application/x-mobipocket-ebook": string;
    "image/jpeg": string;
    "text/html": string;
    "text/plain": string;
    "text/plain; charset=us-ascii": string;
  };
  id: number;
  languages: string[];

  media_type: string;
  subjects: string[];
  title: string;
  translators: any[];
}
