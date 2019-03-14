from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet
import os
import numpy as np


class RSVPHiddenCubeExperimentDataCollection:

    #sending a string of the imageStim image filename
    def sendStimMarker(self, cur_file):
        self.stim_stream_outlet.push_sample(x=[cur_file])

    #call RSVP_trial self.trials times, with self.inter_trial_rest rest periods in between
    def execute_trials(self):
        for trial in range(self.trials):
            core.wait(self.inter_trial_rest)
            self.RSVP_trial()


    #Do a round of RSVP
    def RSVP_trial(self):

        recent_target = True
        stims_since_target = 4

        for image_index in range(self.n_images_per_trial):
            #select image to flip # TODO TBH we should do this before a trial, not during...
            
            if recent_target is False:
                #perhaps we show a target? TODO for now we hardcode 30% chance
                is_target = np.random.randint(low=0, high=10)
                if is_target < 3:
                    #select a target
                    #prepare the CallOnFlip method for first frame of Stim
                    target_index = np.random.randint(low=0, high=len(self.target_images))
                    self.to_present = self.target_images[target_index]
                    self.window.callOnFlip(self.sendTargetMarker, cur_frame=image_index)
                    self.window.callOnFlip(self.sendStimMarker, cur_file=self.to_present.image)
                    recent_target = True
                    stims_since_target = 0
                else:
                    #select a distractor
                    #prepare the CallOnFlip method for first frame of Stim
                    dist_index = np.random.randint(low=0, high=len(self.distract_images))
                    self.to_present = self.distract_images[dist_index]
                    self.window.callOnFlip(self.sendStimMarker, cur_file=self.to_present.image)

            else:
                #select a distractor
                #prepare the CallOnFlip method for first frame of Stim
                dist_index = np.random.randint(low=0, high=len(self.distract_images))
                self.to_present = self.distract_images[dist_index]
                self.window.callOnFlip(self.sendStimMarker, cur_file=self.to_present.image)
                stims_since_target = stims_since_target + 1
                if stims_since_target > 8: #TODO remove magic number hardcode
                    stims_since_target = 0
                    recent_target = False

                

            #flip an image
            for frame in range(self.stim_duration_frames):
                self.to_present.draw()
                self.window.flip()
            #flip a blank
            for frame in range(self.blank_duration_frames):
                self.blank_image.draw()
                self.window.flip()
                           

    #TODO
    #populate targets array with references to ImageStim objects each containing an image in provided target_image_folder
    def load_batch_images(self):
        self.target_images = []
        for file in os.listdir(self.target_image_folder):
            f_name = os.fsdecode(file)
            f_path = os.path.join(self.target_image_folder, f_name)
            cur_image = visual.ImageStim(win=self.window, image=f_path, name=f_name)
            self.target_images.append(cur_image)

    def update_frame_rate(self, nFramesToTest=150):
        
        print("Estimated Frame Duration: {0}".format(self.window.monitorFramePeriod))
        cur_ms_per_frame_arr = self.window.getMsPerFrame(nFrames=nFramesToTest, msg='Assessing Frame Rate...')
        print("Estimated ms per Frame: Avg: {0} Standard Dev: {1}, Median: {2}".format(cur_ms_per_frame_arr[0], cur_ms_per_frame_arr[1], cur_ms_per_frame_arr[2]))                      
        self.cur_ms_per_frame = cur_ms_per_frame_arr[2]

        #this division is what causes difference between desired/actual
        self.stim_duration_frames = int(self.ms_stim_flash_dur / self.cur_ms_per_frame)  
        self.blank_duration_frames = int(self.ms_blank_dur / self.cur_ms_per_frame)

        self.actual_stim_ms = self.stim_duration_frames * self.cur_ms_per_frame
        self.actual_blank_ms = self.blank_duration_frames * self.cur_ms_per_frame
        self.actual_stim_freq = (1000 / (self.actual_stim_ms + self.actual_blank_ms))

        print("Desired Image Flash Duration: {0} ms".format(self.ms_stim_flash_dur))
        print("Desired Blank Flash Duration: {0} ms".format(self.ms_blank_dur))
        print("Actual Image Flash Duration: {0} ms".format(self.actual_stim_ms))
        print("Actual Blank Flash Duration: {0} ms".format(self.actual_blank_ms))
        print("Actual Image Presentation Frequency: {0} Hz".format(self.actual_stim_freq))

    def __init__(self, window,
                 batch_image_folder=os.path.join('D:\Workspace','PULSD','PsychoPy-pylsl-RSVP','images','batch'),
                 blank_image_path=os.path.join('D:\Workspace','PULSD','PsychoPy-pylsl-RSVP','images','blank','black.png'),
                 trials=16,
                 inter_trial_rest=4,
                 n_images_per_trial=25,
                 rest_after_target_length=8,
                 ms_per_frame=20,
                 ms_stim_flash_dur=250,
                 ms_blank_dur=50):

        self.window=window

        self.batch_image_folder = batch_image_folder
        self.blank_image_path = blank_image_path
        self.blank_image = visual.ImageStim(win=self.window, image=self.blank_image_path, name='blank')
        self.to_present = self.blank_image
        self.target_images = []
        self.distract_images = []
        
        #PyLSL streams
        self.stim_stream_info = StreamInfo(name='stim_stream', type='Markers', channel_count=1, channel_format='string', source_id='psychopyStimuli')
        self.stim_stream_outlet = StreamOutlet(self.stim_stream_info)
                
        self.trials = trials
        self.inter_trial_rest = inter_trial_rest #seconds

        self.n_images_per_trial = n_images_per_trial
        self.rest_after_target_length = rest_after_target_length #units? frames or stimuli or time?

        self.ms_per_frame = ms_per_frame
        self.ms_stim_flash_dur = ms_stim_flash_dur
        self.ms_blank_dur = ms_blank_dur
        
        self.stim_duration_frames = 0
        self.blank_duration_frames = 0
        self.cur_ms_per_frame = 0.0
        
        self.actual_stim_ms = 0.0
        self.actual_blank_ms = 0.0
        self.actual_stim_freq = 0.0

        self.update_frame_rate()
        self.load_batch_images()
        
        
if __name__=='__main__':

    win = visual.Window([1600,800],monitor="ASUSLaptopMonitor", units="norm", checkTiming=True)

    RSVPExperiment = RSVPHiddenCubeExperimentDataCollection(win)

    while len(event.getKeys()) < 1:
        core.wait(1.0)

    RSVPExperiment.execute_trials()
