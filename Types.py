import struct

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




if __name__ == '__main__':
    data = varint(1)
    print(data)
    data = varint_int(data)
    print(data)

    data = varlong(2147483647)
    print(data)
    data = varlong_int(data)
    print(data)





