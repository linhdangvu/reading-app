import concurrent.futures

# If we want to return data => returnStatus = True 
# If not => funnction will show empty list
# type = 1 => list , type = 2 => object
def baseThreadPool(loopList, callback, returnStatus=False, type = 1):
    data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for item in loopList:
            futures.append(executor.submit(callback, item))
        if returnStatus:
            for future in concurrent.futures.as_completed(futures):
                if type == 1:
                    data.append(future.result())
                else: 
                    data += future.result()
    return data