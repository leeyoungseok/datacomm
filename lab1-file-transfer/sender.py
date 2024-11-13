import time

hasSentComplete = "0"
status = "0"
DATAFILE = "data"
SIGNALFILE = "signal"
gotData = False

#input_string = "Hello, World!"
input_string = input("Input string: ")

bit_msg = ''.join([bin(ord(ch))[2:].zfill(8) for ch in input_string])
i = 0

print("Bit string to send: " + str(bit_msg))
while hasSentComplete == "0":
    time.sleep(.01)
    #print("Loop: {}/{}".format(str(i), str(len(bit_msg))))
    #print("Progess: {}/100".format(str(int(i/len(bit_msg)*100))))
    with open(SIGNALFILE) as f:
        status = f.read()
    if status == "1": # receiver got data and is waitfing for new data
        with open(DATAFILE, "w") as f:
            f.write(str(bit_msg[i]))
            f.close()
        i+= 1
    with open(SIGNALFILE, "w") as f:
        f.write(str(0)) # receiver has not received data and let's wait for
        f.close()
    if i == len(bit_msg): # end of string
        hasSentComplete = 1
        print("Data sent: " + str(bit_msg))
time.sleep(2)
with open(SIGNALFILE, "w") as f:
    f.write(str(2))
    f.close()