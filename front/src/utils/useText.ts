export default function checkTextLong(text: string) {
  if (text.split("").length >= 50) {
    return text.slice(0, 51) + "...";
  }
  return text;
}
