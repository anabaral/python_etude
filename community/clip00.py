from PIL import ImageGrab
im = ImageGrab.grabclipboard()
im.resize((round(im.width*1.25) , round(im.height*1.25) )).save('./00.png')
