# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 20:48:15 2021

@author: FrizzleFry
"""

class SaltyStruct:
    def __init__(self, **kwds):        
        self.__dict__.update(kwds) 
    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k,v) in vars(self).items()]
        return '%s(%s)' % ( self.__class__.__qualname__, ', '.join(args) )
    
