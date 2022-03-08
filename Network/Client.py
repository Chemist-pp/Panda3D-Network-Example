# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 21:33:33 2022

@author: FrizzleFry
"""


from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from Network.NetworkConstants import MSG

from panda3d.core import NetDatagram
from panda3d.core import DatagramIterator

import time

class Client():
    def __init__(self):

        
        self.cmgr = QueuedConnectionManager()
        self.crdr = QueuedConnectionReader(self.cmgr,0)
        self.cwrt = ConnectionWriter(self.cmgr,0)
        self.conn = None
        
        self.handlers = {
                MSG.CHAT: self.rcvChat,
                MSG.SEQUIT: self.shutdown,
            }
        
        return
    
    def poll(self,task):
        if self.crdr.dataAvailable():
            dgram = NetDatagram()
            if self.crdr.getData(dgram):
                self.parse(dgram)
                
        return task.cont
    
    def chat(self, msg):
        
        dgram = NetDatagram()
        
        dgram.addUint8(MSG.CHAT)
        dgram.addString(msg)
        
        self.cwrt.send(dgram, self.conn)
        
    def rcvChat(self,data):
        amsg = data.getString()
        print(amsg)
              
                
    def parse(self,dgram):
        dgIter = DatagramIterator(dgram)
        
        CMD = dgIter.getUint8()
        if CMD in self.handlers.keys():
            self.handlers[CMD](dgIter)       
        return
        
    
    def connect(self,ip,port,password=None):
        
        self.conn = self.cmgr.openTCPClientConnection(ip,port,3000)
        if self.conn:
            
            dgram = NetDatagram()
            dgram.addUint8(MSG.CLAUTH)
            dgram.addString(password)
            self.cwrt.send(dgram,self.conn)
            
            ## Not sure I really need these saved
            self.ip   = ip
            self.port = port
            self.pw   = password
            
            self.crdr.addConnection(self.conn)   
            
            ts = time.time()
            timeout = 10
            
            while not self.crdr.dataAvailable():
                if time.time() - ts > timeout:
                    break
                
            sgram = NetDatagram()        
            if self.crdr.getData(sgram):               
                sgIter =  DatagramIterator(sgram)
                serverResponse = sgIter.getUint8()
                if serverResponse == MSG.SEAUTH:
                    self.id = sgIter.getUint8()
                    return True
                else:
                    print(sgIter.getString())
                    return False
        
            
        return False
    
        
            
    def shutdown(self):  
        print('DISC')
        self.crdr.removeConnection(self.conn)      
        self.cmgr.closeConnection(self.conn)
        
        

    
    
    
    