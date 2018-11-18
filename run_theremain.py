import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from pyo import *
from data_generate import predict


pitchs = []
for i in range(50):
    pitchs.append(0)

pyoServer = Server().boot()
pyoServer.start()
sig = Sine(260, 0).out()
stupidList = []
newFreq = 440


class SampleListener(Leap.Listener):

    # def on_init(self, controller):
    def on_init(self, controller):
        self.newFreq = 0
        self.newMul = 0

    def on_connect(self, controller):
        print "Connected"

    def map_cap(self, value, origin_min, origin_max, target_min, target_max):
        origin_dataLen = origin_max - origin_min
        target_dataLen = target_max - target_min
        ret_val = target_min + target_dataLen*(value-origin_min)/origin_dataLen

        if ret_val > target_max:
            ret_val = target_max
        elif ret_val < target_min:
            ret_val = target_min
        
        return ret_val

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
        preMappedMidiValue = 0
        for hand in frame.hands:
            if hand.is_left:
                # print("Left Hand Captured...")
                vel = hand.palm_position.y
                #print(vel)
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
                preXPos = pre.palm_position.x

                #origin_max = 250
                #origin_min = -250
                #target_max = 96
                #target_min = 36

                #origin_dataLen = origin_max - origin_min
                #target_dataLen = target_max - target_min

                #preMappedMidiValue = int(target_min + target_dataLen*(preXPos-origin_min)/origin_dataLen)

        pre_status = not(pre_left or pre_right)

        # print("vel is {}".format(vel))
        # print("pitch is {}".format(pitch))
        #origin_max = 250
        #origin_min = -250
        #target_max = 96
        #target_min = 36

        #origin_dataLen = origin_max - origin_min
        #target_dataLen = target_max - target_min
        
        mappedMidiValue = 0
        if right:
            mappedMidiValue = int(self.map_cap(pitch, -50, 250, 60, 84))
            #mappedMidiValue = int(target_min + target_dataLen*(pitch-origin_min)/origin_dataLen)
            #if mappedMidiValue > target_max:
                #mappedMidiValue = target_max
            #elif mappedMidiValue < target_min:
                #mappedMidiValue = target_min

        mappedVeloValue = 0.2
        if left:
            mappedVeloValue = self.map_cap(vel, 100, 250, 0.2, 1)
        #print(mappedVeloValue)
        #sig.mul = mappedVeloValue
        # print(mappedMidiValue)    
        # print(preMappedMidiValue)
        # print(mappedMidiValue)
        frequencyFromMidi = midiToHz(mappedMidiValue)



        # freq = SigTo(frequencyFromMidi, time = 0.5, mul= [1, 1.005])

        if self.newFreq < frequencyFromMidi:
            self.newFreq += 6
        else:
            self.newFreq -= 6

        if self.newMul < mappedVeloValue:
            self.newMul += 0.01
        else:
            self.newMul -= 0.01
        #print(self.newMul)

        sig.setFreq(self.newFreq)
        sig.setMul(self.newMul)
        # if preMappedMidiValue != mappedMidiValue:
        #     sig.setFreq(newFreq)
        # else:

        pitchs.append(mappedMidiValue)

        if len(pitchs) > 50:
            pitchs.pop(0)

        if status and (not pre_status): #status is true, no hand
            # print("trigger the generating now")
            # print(pitchs)
            sig.setFreq(0)
            predict(pitchs)


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
