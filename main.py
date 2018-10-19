from display import Display
from trackbars import Trackbars

name = "target"
target = __import__(name).Target(name)

display = Display()
trackbars = Trackbars(name)

while True:
    frame = display.get_frame()
    frame = target.pre_processing(frame)
