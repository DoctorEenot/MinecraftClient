import Types
import struct



def standart_type_packet(data:bytes):
    return bytes(Types.varint(len(data)))+data


def handshake(server_address,server_port,next_state=2,protocol_version=754):
    '''next state: 1 for status, 2 for login'''
    packet = bytes(Types.varint(0))+bytes(Types.varint(protocol_version))+struct.pack('B',len(server_address))+bytes(server_address,'ascii')+struct.pack('H',server_port)+bytes(Types.varint(next_state))
    return standart_type_packet(packet)

def login(username:str):
    encoded_username = bytes(username,'utf-8')
    if len(encoded_username)<3 or len(encoded_username)> 16:
        raise Exception('length of uesrname must be between 3 an 16 bytes')
    packet = bytes(Types.varint(0))+struct.pack('B',len(encoded_username))+encoded_username
    return standart_type_packet(packet)



if __name__ == '__main__':
    data = handshake('127.0.0.1',25565)
    print(data)
    data = login('DrEenot')
    print(data)