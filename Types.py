import struct
from RBytes import RBytes

def int_byte(number:int):
    
    return bytes((number,))

def varint(number:int)->bytes:
    '''converts int to varint'''    
    number = struct.pack('>i',number)
    to_return = b''

    buf = 0
    counter = 3
    offset = 0
    while True:
        if counter >= 0:
            to_write = (number[counter] & (0b01111111>>offset))<<offset
            to_write += buf
            offset += 1
            buf = number[counter]>>(8-offset)
        else:
            to_write = buf
            buf = 0b0
        found = False
        for i in range(0,counter):
            if number[i] != 0:
                found = True
                break

        if not found:
            if buf == 0:
                to_return += int_byte(to_write)
                break
        to_return += int_byte(to_write|0b10000000)
        counter -= 1

    return to_return
    



def varint_int(number:bytes)->int:
    '''converts varint to int'''
    if len(number)>5 or len(number)<1:
        raise Exception('Wrong size! must be between 1 and 5 bytes')

    to_return = b''

    buf = 0

    for counter in range(len(number)-1,-1,-1):       
        to_return += int_byte((((number[counter]&0b01111111)>>counter)+buf))
        buf = (number[counter] & (0b11111111>>(8-counter)))<<(8-counter)
    
    if to_return[0] == 0:
        to_return = to_return[1:]

    to_return = to_return[::-1]

    for i in range(4-len(to_return)):
        to_return += b'\x00'

    to_return = struct.unpack('i',to_return)[0]

    return to_return





def varlong(number:int)->bytes:
    '''converts int to varint'''    
    number = struct.pack('>q',number)
    to_return = b''

    buf = 0
    counter = 7
    offset = 0
    while True:
        if counter >= 0:
            to_write = (number[counter] & (0b01111111>>offset))<<offset
            to_write += buf
            offset += 1
            buf = number[counter]>>(8-offset)
        else:                        
            offset = 0
            to_write = (buf & (0b01111111>>offset))<<offset            
            offset += 1
            buf = buf>>(8-offset)            
            

        found = False
        for i in range(0,counter):
            if number[i] != 0:
                found = True
                break

        if not found:
            if buf == 0:
                to_return += int_byte(to_write)
                break
        to_return += int_byte(to_write|0b10000000)
        counter -= 1

    return to_return
    



def varlong_int(number:bytes)->int:
    '''converts varint to int'''
    if len(number)>10 or len(number)<1:
        raise Exception('Wrong size! must be between 1 and 10 bytes')

    to_return = b''

    buf = 0

     
    for counter in range(len(number)-1,-1,-1):  
        if counter >8:
            to_return += int_byte((((number[counter]&0b01111111)>>abs(8-counter))+buf)) 
            buf = (number[counter] & (0b11111111>>(abs(len(number)-1-counter))))<<(abs(len(number)-1-counter))
        else:
            to_return += int_byte((((number[counter]&0b01111111)>>counter)+buf))       
            buf = (number[counter] & (0b11111111>>(8-counter)))<<(8-counter)
    
    if len(number)==9:
        to_return = to_return[1:]
    elif len(number)==10:
        to_return = to_return[2:]

    to_return = to_return[::-1]

    for i in range(8-len(to_return)):
        to_return += b'\x00'

    to_return = struct.unpack('q',to_return)[0]

    return to_return

X_Z_OFFSET = RBytes(b'\x03\xff\xff\xff')
Y_OFFSET = RBytes(b'\x0f\xff')


def position(x:int,y:int,z:int)->RBytes:
    '''encodes ints to position'''
    global X_Z_OFFSET, Y_OFFSET  
    
    if x > 33554431 or x<-33554432:
        raise Exception('X must be between -33554432 and 33554431')
    elif z > 33554431 or z < -33554432:
        raise Exception('Z must be between -33554432 and 33554431')
    elif y > 2047 or y < -2048:
        raise Exception('Y must be between -2049 and 2048')

    x = RBytes(struct.pack('>q',x))
    z = RBytes(struct.pack('>i',z))
    y = RBytes(struct.pack('>h',y))

    to_return = ((x & X_Z_OFFSET)<<38) | ((z & X_Z_OFFSET).unsized_lshift(12)) | (y & Y_OFFSET)
    
    return to_return

def decode_position(input:RBytes)->tuple:
    '''decodes array 64 bits into x,y,z'''
    x = struct.unpack('>i',bytes((input >> 38))[-4:])[0]
           
    if x >= 2**25:
        x -= 2**26
            
    y = struct.unpack('>h',bytes((input & Y_OFFSET)[-2:]))[0]
    if y >= 2**11:
        y -= 2**12

    z = struct.unpack('>i',bytes((input<<26)>>38)[-4:])[0]
    if z >= 2**25:
        z -= 2**26

    return x,y,z

def fixed_point(number:float):
    '''converts to fixed point number representation'''
    conv = int(number * 32)
    return struct.pack('i',conv)


def fixed2float(number:bytes):
    '''converts fixed_point to float'''
    unpacked = struct.unpack('i',number)[0]
    return unpacked/32



if __name__ == '__main__':
    data = varint(1)
    print(data)
    data = varint_int(data)
    print(data)

    data = varlong(2147483647)
    print(data)
    data = varlong_int(data)
    print(data)

    data = position(33554431,-2048,33554431)
    print(data)

    data = decode_position(data)
    print(data)

    data = fixed_point(70.78125)
    print(data)

    data = fixed2float(data)
    print(data)





