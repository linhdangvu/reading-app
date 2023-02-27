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

export const sendData = async (url: string, data: any) => {
  try {
    const sendData = await axios.post(url, data, { headers: dataHeaders });
    console.log(sendData.data);
    return sendData.data;
  } catch (e: any) {
    console.log(e);
    return [];
  }
};
