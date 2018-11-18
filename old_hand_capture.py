

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

pitchs = []
for i in range(50):
    pitchs.append(64)

class SampleListener(Leap.Listener):


    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        # print "Frame available"
        frame = controller.frame() # controller is a Leap.Controller object
        previous = controller.frame(1)
        vel = 64
        pitch = 64

        left = False
        right = False
        pre_left = False
        pre_right = False
        for hand in frame.hands:
            if hand.is_left:
                # print("Left Hand Captured...")
                vel = hand.palm_position.y
                left = True
            if hand.is_right:
                # print("Right Hand Captured...")
                pitch = hand.palm_position.x
                right = True
        status = not(left or right)

        for pre in previous.hands:
            if pre.is_left:
                pre_left = True
            if pre.is_right:
                pre_right = True
        pre_status = not(pre_left or pre_right)

        # print("vel is {}".format(vel))
        # print("pitch is {}".format(pitch))
        pitchs.append(pitch)
        if len(pitchs) > 50:
            pitchs.pop(0)
        if status and (not pre_status): #status is true, no hand
            print("trigger the generating now")
            print(pitchs)
            # predict(pitchs)

def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
