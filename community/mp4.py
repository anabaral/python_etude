import cv2, sys

if len(sys.argv) > 1:
  path = sys.argv[1]
else:
  path = './01.mp4'

v = cv2.VideoCapture(path)
width = v.get(cv2.CAP_PROP_FRAME_WIDTH)
height = v.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f'<embed src="" width="{width}" height="{height}" />')
