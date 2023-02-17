export const toApexChart2 = (data1: any[], data2: any[]) => {
  return data1.map((item: any, index: number) => {
    return { x: item, y: data2[index] };
  });
};

export const toApexChart = (data: any[]) => {
  return data.map((item: any) => {
    const key: any = Object.keys(item).pop();
    return { x: key, y: item[key] };
  });
};
