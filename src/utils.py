import socket


''' Send given value to the given address. '''
def send_value(to_addr, value):
    if not to_addr:
        print("Remote Address Not Set!")
        return

    msg = "VALUE:%d" % value
    print("Sending '%s' to '%s'" % (msg, to_addr))
    s = socket.socket()
    s.connect(to_addr)
    s.send(bytes(msg+"\r\n\r\n", 'utf8'))
    # return_msg = str(s.recv(64), 'utf8')
    # if return_msg == "OK":
    #     print("Message Received!")
    # else:
    #     print("Error: '%s'" % return_msg)
    s.close()


''' Watch network for incoming value and send it to callback function. '''
def watch_for_value(my_addr, callback):
    if not my_addr:
        print("Local Address Not Set!")
        return

    s = socket.socket()
    s.bind(my_addr)
    s.listen(1)
    value = -1
    while True:
        cl, addr = s.accept()
        print('Client connected from', addr[0])
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
            # print("Received: '%s'" % line)
            if line[:6] == b'VALUE:':
                value = int(line[6:])
                break
        cl.send("OK")
        cl.close()
        # print("Value = %d" % value)
        if value >= 0:
            callback(value)
