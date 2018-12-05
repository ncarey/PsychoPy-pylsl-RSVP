from psychopy import visual, core, event
from pylsl import StreamInfo, StreamOutlet
import os

class RSVPTrainingDataCollection:

    #TODO - should be sending a string of the imageStim image filename...
    def sendStimMarker(self, cur_frame=1):
        self.stim_stream_outlet.push_sample(x=[cur_frame])

    def sendTargetMarker(self, cur_frame=1):
        self.target_stream_outlet.push_sample(x=[cur_frame])

    #call RSVP_trial self.trials times, with self.inter_trial_rest rest periods in between
    def execute_trials(self):
        for trial in range(self.trials):
            core.wait(self.inter_trial_rest)
            self.RSVP_trial()


    #TODO Do a round of RSVP
    def RSVP_trial(self):

        for image_index in range(self.n_images_per_trial):
            #select image to flip
    
           
            #prepare the CallOnFlip method for first frame of Stim

            #flip an image
            for frame in range(self.stim_duration_frames):

            #flip a blank
            for frame in range(self.blank_duration_frames):
                self.blank_image.draw()
                self.window.flip()
                           


    #TODO populate distractor array with references to imageStim objects each contianing an image in provided target_image_folder
    def load_distractor_images(self):



    #TODO populate targets array with references to ImageStim objects each containing an image in provided target_image_folder
    def load_target_images(self):

        

    def update_frame_rate(self, nFramesToTest=250):
        
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

    def __init__(self, window, target_image_folder, distract_image_folder,
                 blank_image_path=os.path.join('D:\Workspace','PULSD','PsychoPy-pylsl-RSVP','images','blank','black.png'),
                 trials=4,
                 inter_trial_rest=4,
                 n_images_per_trial=20,
                 rest_after_target_length=8,
                 ms_per_frame=20,
                 ms_stim_flash_dur=250,
                 ms_blank_dur=50):

        self.window=window

        self.target_image_folder = target_image_folder
        self.distract_image_folder = distract_image_folder
        self.blank_image_path = blank_image_path
        self.blank_image = visual.ImageStim(win=self.window, image=self.blank_image_path, name='blank')
        
        #PyLSL streams
        self.stim_stream_info = StreamInfo(name='stim_stream', type='Markers', channel_count=1, channel_format='int32', source_id='psychopyStimuli')
        self.stim_stream_outlet = StreamOutlet(self.stim_stream_info)
        
        self.target_stream_info = StreamInfo(name='target_stream', type='Markers', channel_count=1, channel_format='int32', source_id='psychopyTargets')
        self.target_stream_outlet = StreamOutlet(self.target_stream_info)
        
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

        

        
