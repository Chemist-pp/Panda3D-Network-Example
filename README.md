# SaltyStudios

Network classes are asynchronous and threaded using panda3d modules.
The panda3d class calls into c++ threading modules and has some modest performance improvements, reportedly.
The use is directly mirroring python threading.  To use python threading, just replace
  from direct.stdpy import threading
  with
  import threading
  
  
