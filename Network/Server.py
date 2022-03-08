# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 20:41:17 2022

@author: FrizzleFry
"""

from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter

from panda3d.core import PointerToConnection
from panda3d.core import NetAddress

from panda3d.core import NetDatagram
from panda3d.core import DatagramIterator


from Network.NetworkConstants import MSG



class Server():
    def __init__(self,port,password=None):
        
         
        self.port = port
        self.pw = password
        
        self.newconn      = {}
        self.connections  = {}
        self.cid = 0
        
        self.maxplayers = 4
        
        self.cmgr = QueuedConnectionManager()
        self.clsn = QueuedConnectionListener(self.cmgr,0)
        self.crdr = QueuedConnectionReader(self.cmgr,0)
        self.nrdr = QueuedConnectionReader(self.cmgr,0)
        self.cwrt = ConnectionWriter(self.cmgr,0)
        
        self.socket = self.cmgr.openTCPServerRendezvous(self.port, 10)
        
        self.clsn.addConnection(self.socket)
        
        self.handlers = {
                MSG.CHAT: self.chat,
                MSG.CLQUIT: self.delClient,               
            }
        
        return
    
    
    def listen(self, task):
        
        if self.clsn.newConnectionAvailable():            
            rndz = PointerToConnection()
            addr = NetAddress()
            conn = PointerToConnection()            
            
            if self.clsn.getNewConnection(rndz,addr,conn):
                conn = conn.p()
                if (len(self.connections) + len(self.newconn)) < self.maxplayers:                
                    while self.cid in self.connections.keys() or self.cid in self.newconn.keys():
                        self.cid += 1
                        self.cid %= 10                                        
                    self.newconn[self.cid] = conn       
                    self.nrdr.addConnection(conn)
                    
        ##Perhaps I could spawn a new task for authentication
        ##But the listener gets bored I heard so I give
        ##him something extra to do.  He also makes sure
        ##The client connectiong knows what is going on
        ##If the client does not authenticate properly, bye
        
        if self.nrdr.dataAvailable():
            
            agram = NetDatagram()
            if self.nrdr.getData(agram):
                conn = agram.getConnection()
                cid = 0
                for ids in self.newconn:
                    if self.newconn[ids] == conn:
                        cid = ids                        
                        break
          
                rgram = NetDatagram()
                
                agIter = DatagramIterator(agram)
                CMD = agIter.getUint8()
                bSuccess = False
                
                if CMD == MSG.CLAUTH:                 
                    if self.pw is not None:
                        PW = agIter.getString()                       
                        if PW != self.pw:  
                            
                            #Fail
                            rgram.addUint8(MSG.SEQUIT)
                            rgram.addString('Bad Credentials')                                                  
                        else:   
                            bSuccess = True                                                  
                    else:
                        #automatic success, no pw
                        bSuccess = True             
                else:
                    rgram.addUint8(MSG.SEQUIT)
                    rgram.addString('Bad Request')                           
               
                    
                if bSuccess:
                   rgram.addUint8(MSG.SEAUTH)
                   rgram.addUint8(cid)    
                   
                   ##Move connection to connected reader
                   self.crdr.addConnection(conn)
                   self.nrdr.removeConnection(conn)
                   
                   ##Move connection tracking to connection list
                   self.connections[cid] = conn
                   del self.newconn[cid]
                   
                   self.cwrt.send(rgram,conn) 
                else:
                    self.cwrt.send(rgram,conn) 
                    
                    self.nrdr.removeConnection(conn)
                    self.cmgr.closeConnection(conn)
                    del self.newconn[cid]
                
        return task.cont
        
    def poll(self, task):      
        if self.crdr.dataAvailable():
            dgram = NetDatagram()
            if self.crdr.getData(dgram):
                self.parse(dgram)
                
        return task.cont
                
    def parse(self, dgram):
        conn = dgram.getConnection()
        
        dgIter = DatagramIterator(dgram)
        CMD = dgIter.getUint8()
        
        if CMD in self.handlers.keys():
            self.handlers[CMD](conn,dgIter)
            
        return
    
    def shutdown(self):        
        for aconn in self.connections:
            self.crdr.removeConnection(self.connections[aconn])
        self.connections = {}
        
        self.cmgr.closeConnection(self.socket)
        
    
    
    def broadcast(self,msg,exlude=None):
        
        if exlude is None:
            exlude = []
        
        dgram = NetDatagram()
        dgram.addUint8(MSG.CHAT)
        dgram.addString(msg)
        
        for aconn in self.connections:
            if self.connections[aconn] not in exlude:
                #print('Sending msg to client {} of {}.'.format(aconn+1,len(self.connections)))
                self.cwrt.send(dgram,self.connections[aconn])
            #else:
               #print('Not sending msg to client {} of {}.'.format(aconn+1,len(self.connections)))
        
    ## Call backs   
    def chat(self,conn,data):
        msg = data.getString()
        print("Broadcasting Msg!")
        self.broadcast(msg,[conn])
        
        
    def delClient(self,conn,data):
       for aconn in self.connections:
           if self.connections[aconn] == conn:
               self.crdr.removeConnection(conn)
               self.cmgr.closeConnection(conn)
               del self.connections[aconn]
               
               break
       return 
                   
    