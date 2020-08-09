import cv2
import numpy as np

# function to convert data to binary
def to_bin(data):
    # data to binary as string
    if isinstance(data,str):
        return ''.join([format(ord(i),"08b") for i in data])
    elif isinstance(data,bytes) or isinstance(data,np.ndarray):
        return [ format(i,"08b") for i in data]
    elif isinstance(data,int) or  isinstance(data,np.uint8):
        return format(data,"08b")
    else:
        raise TypeError("Type not supported.")


# encoding data to image

def encode(image_name,secret_data):
    # read the image
    image=cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes=image.shape[0]*image.shape[1]*3//8
    print("[*] Maximum bytes to encode",n_bytes)
    if len(secret_data)>n_bytes:
        raise ValueError("Insufficient bytes, need bigger image or less data")
    print("Encoding data...")
    # add stopping criteria
    secret_data+="===="
    data_index=0
    # convert to binary
    b_secret_data=to_bin(secret_data)
    # size of data to hide
    data_len=len(b_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary
            r,g,b=to_bin(pixel)
            # modify least significant bit if there is data to store
            if data_index<data_len:
                # least significant red pixel bit
                pixel[0]=int(r[:-1]+b_secret_data[data_index],2)
                data_index+=1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + b_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + b_secret_data[data_index], 2)
                data_index += 1
             # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

# decoder

def decode(image_name):
    print("Decoding...")
    # read the image
    image=cv2.imread(image_name)
    b_data=""
    for row  in image:
        for pixel in row:
            r,g,b=to_bin(pixel)
            b_data+=r[-1]
            b_data+=g[-1]
            b_data+=b[-1]
    # split by 8 bits
    all_bytes=[b_data[i:i+8] for i in range(0,len(b_data),8)]
    # converg from bits to characters
    decoded_data=""
    for byte in all_bytes:
        decoded_data+=chr(int(byte,2))
        if decoded_data[-5:]=="====":
            break
    return decoded_data[:-5]

if __name__=="__main__":
    op=input("1.Encoding \n 2.Decoding")
    if op==1:
        input_image="image.PNG"
        secret_data="how are you"
        encoded_image = encode(image_name=input_image, secret_data=secret_data)
        cv2.imwrite("output_image", encoded_image)

    elif op==2:
        image="output_image.PNG"
        decoded_data=decode(image)
        print("Decoded mesage: ",decoded_data)
        