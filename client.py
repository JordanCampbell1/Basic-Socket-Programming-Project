# Client to implement a simple program to send two prime numbers to a
# server. The server will compute their LCM and send back to the client.
# If the server-calculated LCM matches what the client computes, the 
# client will send a 200 OK status code to the server. Otherwise a
# 400 Error code is sent to the server.

# Author: fokumdt
# Last modified: 2023-10-09
#!/usr/bin/python3

import socket
import sys

def findLCM(num1, num2):
  greater = max(num1, num2)
  while True:
    if((greater % num1 == 0) and (greater % num2 == 0)):
      clientlcm = greater
      return clientlcm
    greater += 1


def serverHello():
  """Generates server hello message"""
  status = "100 Hello"
  return status

def AllGood():
  """Generates 200 OK"""
  status = "200 OK"
  return status

def ErrorCondition():
  """Generates 400 Error"""
  status = "400 Error"
  return status


def PrimeCollect():
  """Accepts a prime number to send to the server"""
  primeNbr = input("Enter a prime number between 1031 and 6397: ")
  return primeNbr

def PrimeMsg(prime1, prime2):
  """Generates the first prime number to send"""
  msg = "105 Primes "+ str(prime1) + " " + str(prime2)
  return msg
  
# s     = socket
# msg   = message being processed
# state = dictionary containing state variables
def processMsgs(s, msg, state):
  
  if msg == "101 Hello Ack":

    print("Sending: " + PrimeMsg(state["num1"], state["num2"]) + "...")  
    s.send(PrimeMsg(state["num1"], state["num2"]).encode())


  elif state["check"] == "107 LCM":  

    primeresponsearray = msg.split()

    clientlcm = state["lcm"]

    lcm = int(primeresponsearray[2])

    if lcm == clientlcm:
      print("Sending: " + AllGood() + "...")
      s.send(AllGood().encode())
    else:
      print("Sending: " + ErrorCondition() + "...")
      s.send(ErrorCondition().encode())
  

  pass

def main():
  """Driver function for the project"""
  args = sys.argv
  if len(args) != 3:
    print("Please supply a server address and port.")
    sys.exit()
  serverHost = str(args[1])  #The remote host
  serverPort = int(args[2])  #The port used by the server
  print("Client of Jordan Campbell")
  print("""
  The purpose of this program is to collect two prime numbers from the client, and then
  send them to the server. The server will compute their LCM and send it back to the
  client. If the server-computed LCM matches the locally computed LCM, the
  clientsends the server a 200 OK status code. Otherwise it sends a 400 error status code,
  and then closes the socket to the server.
  """)
  #Add code to initialize the socket
  msg = serverHello()
  #Add code to send data into the socket
  #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  #  s.connect((serverHost, serverPort))
  #  s.send(msg.encode())

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((serverHost, serverPort))

  print("Sending: " + msg + "...")
  s.send(msg.encode())

  state = {} #...
  #Handle the data that is read through the socket by using processMsgs(s, msg, state)
  
  ackresponse = s.recv(1024).decode()
  print("Received: " + ackresponse)
  primenum1 = int(PrimeCollect())
  primenum2 = int(PrimeCollect())
  clientlcm = findLCM(primenum1, primenum2)
  #print("This is the value of: " ,clientlcm)
  state['lcm'] = clientlcm #could be calculated in the next section
  state['num1'] = primenum1
  state['num2'] = primenum2
  processMsgs(s, ackresponse, state)

  primeresponse = s.recv(1024).decode()
  print("Received: " + primeresponse)
  if primeresponse == "501 Not Prime":
    s.close()
  else:
    primeresparr = primeresponse.split()
    state["check"] = primeresparr[0] + " " + primeresparr[1]
    processMsgs(s, primeresponse, state)



  #Close the socket
  s.close()
if __name__ == "__main__":
    main()
  