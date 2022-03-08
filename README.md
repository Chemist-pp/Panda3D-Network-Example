# SaltyStudios

Network classes listening and polling using the Panda3D task manager.

Currently the server polling threading is managing the message handling.


taskMgr.setupTaskChain('serverChain', numThreads = 1, threadPriority = 1)

server = Server(port, possword)

taskMgr.add(server.listen,'listen',-39,taskChain='serverChain')

taskMgr.add(server.poll,'poll',-40,taskChain='serverChain')

client = Client()

if client.connect(ip,port,password):    

            print("connected with id",client.id)
            
            taskMgr.add(client.poll,'client-poll',-38)
            
  

### Implement Call Backs


1.  Add int to Network.NetworkConstants MSG 
2.  Add key/func to self.handlers: 
3.  Implement recv function, callbackfnc(conn, DatagramIterator)
4.  Implement send function to construct datagram for recv
5.  Send function should start with dgram.addUint8(command)


  
