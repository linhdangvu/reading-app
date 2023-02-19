import axios from "axios";

const dataHeaders: any = {
  Accept: "application/json",
  "Content-Type": "application/json",
};

export const getBooks = async (url: string) => {
  try {
    const data = await axios.get(url);
    // console.log(data.data);
    return data.data;
  } catch (e: any) {
    console.log(e);
    return [];
  }
};

export const sendSearchData = async (url: string, wordData: string) => {
  try {
    const sendData = await axios.post(
      url,
      { word: wordData },
      { headers: dataHeaders }
    );
    console.log(sendData.data);
    return sendData.data;
  } catch (e: any) {
    console.log(e);
    return [];
  }
};

const data = {
  id: 7,
  title: "The Mayflower Compact",
  authors: [],
  translators: [],
  subjects: [
    "Massachusetts -- History -- New Plymouth, 1620-1691 -- Sources",
    "Mayflower Compact (1620)",
    "Pilgrims (New Plymouth Colony)",
  ],
  bookshelves: [],
  languages: ["en"],
  copyright: false,
  media_type: "Text",
  formats: {
    "application/x-mobipocket-ebook":
      "https://www.gutenberg.org/ebooks/7.kf8.images",
    "application/epub+zip": "https://www.gutenberg.org/ebooks/7.epub3.images",
    "text/html": "https://www.gutenberg.org/ebooks/7.html.images",
    "image/jpeg": "https://www.gutenberg.org/cache/epub/7/pg7.cover.medium.jpg",
    "text/plain; charset=us-ascii": "https://www.gutenberg.org/files/7/7.txt",
    "text/plain": "https://www.gutenberg.org/ebooks/7.txt.utf-8",
    "application/rdf+xml": "https://www.gutenberg.org/ebooks/7.rdf",
  },
  download_count: 93,
};
