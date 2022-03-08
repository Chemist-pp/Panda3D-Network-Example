# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 19:34:55 2022

@author: FrizzleFry
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, CompassEffect

import SaltyMenus as sm
from Network.Server import Server
from Network.Client import Client


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        
        self.port     = 22501
        self.ip       = '127.0.0.1'
        self.server   = None
        self.client   = None
        self.password = 'SaltyPass'
        
        self.disableMouse()
        
        wProp = WindowProperties()
        wProp.setSize(800,600)
        self.win.requestProperties(wProp)
        
        self.state = 'MAIN'
      
        taskMgr.setupTaskChain('serverChain', numThreads = 1, threadPriority = 1)
        '''
        taskMgr.setupTaskChain('chain_name', numThreads = None, tickClock = None,
                       threadPriority = None, frameBudget = None,
                       frameSync = None, timeslicePriority = None)
        
        '''
        self.updateTask = self.taskMgr.add(self.update,'update')
        
        self.mainmenu = sm.menu('Main Menu',{
                'Host':self.hostGame,
                'Join':self.joinGame,
                'Quit':self.quitApp
            })
        
        self.exitFunc = self.cleanup
        
        self.running = True
        
        self.mainmenu.show()
        
        return
    
    def update(self,task):
        
        dt = globalClock.getDt()
        
        
        if not self.running:
            return task.done
        
        return task.cont
        
        
    def hostGame(self):
        print('Host')
        
        self.server = Server(self.port,self.password)
        self.taskMgr.add(self.server.listen,'listen',-39,taskChain='serverChain')
        self.taskMgr.add(self.server.poll,'poll',-40,taskChain='serverChain')
        
        self.joinGame()
        
        return
        
    
    def joinGame(self):
        print('Join')
        
        self.client = Client()
        if self.client.connect(self.ip,self.port,self.password):    
            print("connected with id",self.client.id)
            self.taskMgr.add(self.client.poll,'client-poll',-38)            
        else:
            print('Failed to connect!')
            
        return
        
    def quitApp(self):
        base.userExit()
        
        return
    
    
    def cleanup(self):
        
        if self.server is not None:
            self.server.shutdown()
            self.server = None
            
        
        return
        
    
if __name__ == '__main__':
    app = App()
    app.run()
    
        