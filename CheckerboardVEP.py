from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet
import os
import numpy as np

class CheckerboardVEP:

    def sendMarker(self, cur_frame):
        self.outlet.push_sample(x=[cur_frame])

    def stimulate(self):

        for frame in range(self.trial_duration_frames):
            #check if its time for reversal
            if frame % self.rev_duration_frames == 0:
                self.grating.contrast = self.grating.contrast * -1
                self.window.callOnFlip(self.sendMarker, cur_frame=frame)
            self.grating.draw()
            self.window.flip()

            
        #cleanup
        self.window.close()
        core.quit()

    def __init__(self, window, ms_per_frame, reversal_freq, trial_duration):
        self.window = window
        self.ms_per_frame = ms_per_frame
        self.target_freq = reversal_freq

        self.rev_duration_ms = (1.0 / self.target_freq) * 1000
        #this division is what causes difference between desired/actual
        self.rev_duration_frames = int(self.rev_duration_ms / self.ms_per_frame)  


        self.actual_rev_dur_ms = self.rev_duration_frames * self.ms_per_frame
        self.actual_rev_freq = (1000 / self.actual_rev_dur_ms)

        print("Desired reversal frequency: {0} Hz".format(self.target_freq))
        print("Desired ms duration per reversal: {0} ms".format(self.rev_duration_ms))
        print("Actual frames per reversal: {0} frames".format(self.rev_duration_frames))
        print("Actual ms duration per reversal: {0} ms".format(self.actual_rev_dur_ms))
        print("Actual reversal frequency: {0} Hz".format(self.actual_rev_freq))

        self.trial_duration_seconds = trial_duration
        self.trial_duration_frames = int((self.trial_duration_seconds * 1000) / self.ms_per_frame)

        
        #create 8x8 checkerboard texture
        checkTex = np.array([
                [ 1, -1, 1, -1, 1, -1, 1, -1],
                [ -1, 1, -1, 1, -1, 1, -1, 1],
                [ 1, -1, 1, -1, 1, -1, 1, -1],
                [ -1, 1, -1, 1, -1, 1, -1, 1],
                [ 1, -1, 1, -1, 1, -1, 1, -1],
                [ -1, 1, -1, 1, -1, 1, -1, 1],
                [ 1, -1, 1, -1, 1, -1, 1, -1],
                [ -1, 1, -1, 1, -1, 1, -1, 1]])

        self.grating = visual.GratingStim(win=self.window, tex=checkTex, size=1.5, pos=[0,0])
        self.info = StreamInfo(name='test_stream', type='Markers', channel_count=1, channel_format='int32', source_id='psychopyStimuli')
        self.outlet = StreamOutlet(self.info)
 


if __name__=='__main__':

    win = visual.Window([1920,1080],monitor="testMonitor", units="norm", checkTiming=True)
    print("Estimated Frame Duration: {0}".format(win.monitorFramePeriod))
    cur_ms_per_frame = win.getMsPerFrame(nFrames=300, msg='Assessing Frame Rate...')
    print("Estimated ms per Frame: Avg: {0} Standard Dev: {1}, Median: {2}".format(cur_ms_per_frame[0], cur_ms_per_frame[1], cur_ms_per_frame[2]))                      

    reversal_freq = 5

    trial_duration = 30 #seconds
    
    check = CheckerboardVEP(win, cur_ms_per_frame[2], reversal_freq, trial_duration)
    check.stimulate()
