function clearArray(array: any) {
  while (array.length > 0) {
    array.pop()
  }
}
function addArray(arrayMain: any, arrayAdd: any) {
  for (const i in arrayAdd) {
    arrayMain.push(arrayAdd[i])
  }
}

export { clearArray, addArray }
