#!/usr/bin/python3

import socket
from timeit import default_timer as timer

# If you set this to false, it'll dump everything.
checkAccessCode=True

inPacket=False
AccessCode="1010101010101010"
syncword=''
# Ultimately if an alternating 101010 access code is used followed by a sync word,
# the packet header is actually the combination of the two.  So update the
# Access code to reflect that.
AccessCode=AccessCode + syncword
# typically bits want to alternate to keep the clock sync'd
deadDetectionSequence='000000000'  # This should be something.  At least 0000 or 1111
# Also, we need to make sure we let the buffer reach at least a min size or 
# we could miss markers
minBuffLength=len(AccessCode)
if len(deadDetectionSequence) > minBuffLength:
    minBuffLength=len(deadDetectionSequence)
# The last buffer quality check is a timer.  Once a packet is no longer detected,
# If we still haven't detected a new access code, we'll use the timer to 
# flush other bad data from the buffer to keep it from filling up
maxTimeWithoutAC=1  # in seconds
lastEndOfPacket=timer()

buffer=''

def ProcessBuffer():
    global inPacket
    global AccessCode
    global syncword
    global deadDetectionSequence
    global buffer
    global maxTimeWithoutAC
    global lastEndOfPacket
    
    if (len(buffer) < minBuffLength):
        return

    keepProcessing=True
    
    while keepProcessing:
        keepProcessing=False  # Used at the end if we have another access code in an alreaday processing stream
        
        # Look through buffer for access code.  
        # If we're not in a packet and we see dead bytes, just delete them.
        if not inPacket:
            # look for access code.
            posAC=buffer.find(AccessCode)
            
            if posAC >= 0:
                # strip off leaders
                buffer=buffer[posAC:]
                inPacket=True
                print('\n<Packet Detected>')
            else:
                # Just clear the buffer
                buffer=''

        # Now if the packet ends mid-stream, let's get rid of that.
        posDeadSpace=buffer.find(deadDetectionSequence)
        if posDeadSpace >=0:
            if posDeadSpace==0:
                # dump all dead space, which could clear the buffer.  In any case let the next cycle happen to fill the buffer with more data
                buffer=buffer.lstrip('0')
                inPacket=False
                if len(buffer) > 0:
                    keepProcessing=True
                    continue
            else:
                # Now what if it's in the middle?  Print what we have up till then, remove the dead space, then save the rest for the next cycle
                if inPacket:
                    print(buffer[0:posDeadSpace], end='')
                    buffer=buffer[posDeadSpace+len(deadDetectionSequence):]
                    buffer=buffer.lstrip('0')  # If the zero's were longer than dead space, remove the extras
                    lastEndOfPacket=timer()
                    inPacket=False
                    
     
        if inPacket and len(buffer)>0:
            matchingChars=MayEndWithDeadCode()
            
            if matchingChars==0:
                # Have access code, but haven't found dead space yet so print what we have and flush the buffer
                print(buffer, end='')
                buffer=''
            else:
                tmpBuff=buffer[0:len(buffer)-matchingChars]
                print(tmpBuff, end='')
                buffer=buffer[len(buffer)-matchingChars:]
        
        # Check if there's another packet starting.  If so keep processing.
        if buffer.find(AccessCode) >=0:
            keepProcessing=True

        if (not inPacket) and ((timer()-lastEndOfPacket)>maxTimeWithoutAC):
            buffer=''

def MayEndWithDeadCode():        
    if len(deadDetectionSequence)==0:
        return 0
        
    # Need to see if any part of the beginning of the dead code lines up with the end of the buffer
    MatchingChars=0
    buffstart=len(buffer)-len(deadDetectionSequence)
    if buffstart < 0:
        buffstart=0
    testString=buffer[buffstart:]
    
    for i in range(1, len(testString)):
        left_dead=deadDetectionSequence[0:i]
        right_test=testString[len(testString)-i:]
        
        if left_dead ==right_test:
            MatchingChars=i
        else:
            break
            
    return MatchingChars
    
    
# Socket parameters
udpport=6543
listen_ip='127.0.0.1'
server_address = (listen_ip, udpport)
print('starting up listener on ',server_address,' on port ', udpport)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)
sock.settimeout(1) # 1 second timeout for blocking recvfrom

# Test Data
# buffer='0000000001010101010101010001100101001000000000000000001010101010101010001100101001000000'
# ProcessBuffer()
# buffer=buffer+'0011111111111111111100000111100011'
# ProcessBuffer()

print('\nwaiting to receive data.  Use CTRL-C to quit.')

try:
    while True:
        try:
            data, address = sock.recvfrom(4096)
        except KeyboardInterrupt:
            sock.close()
            print("\nExiting.")
            exit(0)
        except:
            data=''
            
        if data:
            for byte in data:
                curBit=''
                if byte== 0:
                    curBit='0'
                elif byte== 1:
                    curBit='1'
                elif byte== 2:  # If using access code detection, new packet would have a 2nd bit set
                    curBit='<New Packet>0'
                elif byte==3:
                    curBit='<New Packet>1'

                if checkAccessCode and len(AccessCode)>0:
                    buffer += curBit
                    ProcessBuffer()
                else:
                    print(curBit,end="")
except KeyboardInterrupt:
    sock.close()
    print("Exiting.")
