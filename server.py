# Server to implement a simple program to receive two prime numbers from a
# client. The server will compute their LCM and send it back to the client.
# If the server-calculated LCM matches what the client computes, the client
# will send a 200 OK status code to the server. Otherwise a 400 Error code is
# sent to the server.

# Author: fokumdt
# Last modified: 2023-10-09
#!/usr/bin/python3

import socket
import sys

def checkRange(num):
   if (num <= 6397) and (num >= 1031):
      return True
   else:
      return False

def checkPrime(num):
  if num > 1:
    for i in range(2, num//2):
        # If num is divisible by any number between
        # 2 and n/2, it is not prime
        if (num % i) == 0:
            return False
        else:
          return True
  else:
    return False

def notPrime():
  """When the number received is not a prime number"""
  msg = "501 Not Prime"
  return msg
   
  
def badRequest():
  """When the server receives a message from the client that is unexpected"""
  msg = "500 Bad Request"
  return msg

def clientHello():
  """Generates an acknowledgement for the client hello message"""
  msg = "101 Hello Ack"
  return msg

def generateLCMstring(lcm):
  """Generates the 107 LCM string"""
  msg = "107 LCM " + str(lcm)
  return msg

#s      = socket
#msg    = message being processed
#state  = dictionary containing state variables
def processMsgs(conn, msg, state):
  
  if msg == "100 Hello":
     print("Sending: " + clientHello() + "...")
     conn.send(clientHello().encode())



  elif state["check"] == "105 Primes":
    primearray = msg.split()
    primenums = [int(primearray[2]), int(primearray[3])] 

    if ( checkRange(primenums[0]) ) == True and ( checkRange(primenums[1]) ) == True:
        

      if ( checkPrime(primenums[0]) and checkPrime(primenums[1]) ) == False:
        print("Sending " + notPrime() + "...")
        conn.send(notPrime().encode())
        servstatus = -3
        return servstatus

        #conn.close()

      else:

        if primenums[0] > primenums[1]:
              greater = primenums[0]
        else:
              greater = primenums[1]
        while True:
            if((greater % primenums[0] == 0) and (greater % primenums[1] == 0)):
                lcm = greater
                break
            greater += 1
          
        print("Sending: " + generateLCMstring(lcm) + "...")  
        conn.send(generateLCMstring(lcm).encode())
    else:
       print("Sending: " + badRequest() + "...")
       conn.send(badRequest().encode())
       servstatus = -1
       #"Bad Request Received From Client: 'Out of Range'"
       return servstatus
       #conn.close()
  else:
     print("Sending: " + badRequest() + "...")
     conn.send(badRequest().encode())
     servstatus = -2
     #"Bad Request Received From Client"
     return servstatus
     #conn.close()

  

  #conn.close()

def main():
  """Driver function for the server."""
  args = sys.argv
  if len(args) != 2:
    print ("Please supply a server port.")
    sys.exit()
  HOST = ''              #Symbolic name meaning all available interfaces
  PORT = int(args[1])    #The port on which the server is listening.
  if (PORT < 1023 or PORT > 65535):
    print("Invalid port specified.")
    sys.exit()

  print("Server of Jordan Campbell")
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind socket
    s.bind((HOST,PORT))
    # listen
    s.listen(1)
    print ('The server is ready to receive')

    while True:
      conn, addr = s.accept() # accept connections using socket
      #with conn:
      print("Connected from: ", addr)
      #Process messages received from socket using 
      msg1 = conn.recv(1024).decode()
      print("Received: " + msg1)
      state = {} 
      processMsgs(conn, msg1, state)

      msg2 = conn.recv(1024).decode()
      print("Received: " + msg2)
      msg2arr = msg2.split()
      state["check"] = msg2arr[0] + " " + msg2arr[1]
      servstatus = processMsgs(conn, msg2, state) #checks if any bad request was received from the client via the function

      if servstatus == -1:
         print("Bad Request Received From Client: 'Out of Range'")
         conn.close()
      elif servstatus == -2:
         print("Bad Request Received From Client")
         conn.close()
      elif servstatus == -3:
         print("Bad Request Received From Client: 'One of the Numbers from the Client is not a Prime Number'")
         conn.close()
      else:
        statusmessage = conn.recv(1024).decode()
        print("Received: " + statusmessage)

        #add an if else statement to check if the messgage is empty or not
        conn.close()
      
      print("\n|New Connection can be Accepted|\n")
      
if __name__ == "__main__":
    main()