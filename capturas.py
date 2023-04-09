#Librerias necesarias para la captura de pantalla

import win32gui
import win32ui
import win32con

#Librerias necesarias para controlar el navegador



#w = 1920 # set this
#h = 1080 # set this

def estado():
    w = 600
    h = 530

    bmpfilenamename = "frames/prueba.bmp" #set this

    hwnd = win32gui.FindWindow(None, 'sfasfaf')
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,185), win32con.SRCCOPY)
    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())





