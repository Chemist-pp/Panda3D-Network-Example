# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 19:08:51 2022

@author: FrizzleFry
"""
from direct.gui.DirectGui import DirectDialog, DirectLabel, DirectButton, DGG

def menu(title,btns):
    screen = DirectDialog(frameSize = (-0.6,0.6,-0.8,0.8),
                fadeScreen = 0.4,
                relief = DGG.FLAT)
    
    screen.hide()
    font = loader.loadFont('Assets/Fonts/Wbxkomik.ttf')
    
    btnImgs = (
            loader.loadTexture("Assets/UI/UIButton.png"),
            loader.loadTexture("Assets/UI/UIButtonPressed.png"),
            loader.loadTexture("Assets/UI/UIButtonHighlighted.png"),
            loader.loadTexture("Assets/UI/UIButtonDisabled.png")            
        )   
    
    label = DirectLabel(text=title,
                        parent = screen,
                        scale = 0.07,
                        pos = (0,0,0.5),
                        text_font = font,
                        relief = None)
    
    i = 0
    x = 0.15
    for btn,fnc in btns.items():
        i += 1
        b = DirectButton(text = btn,
                         command = fnc,
                         pos = (0,0,0.5-x*i),
                         parent = screen,
                         scale = 0.07,
                         text_font = font,
                         clickSound = loader.loadSfx("Assets/Sounds/UIClick.ogg"),
                         frameTexture = btnImgs,
                         frameSize = (-4,4,-1,1),
                         text_scale = 0.75,
                         relief = DGG.FLAT,
                         text_pos = (0, -0.2))
        b.setTransparency(True)
        
    return screen
                         

    