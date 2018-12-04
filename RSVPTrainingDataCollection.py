from psychopy import visual, core, event
import pylsl
import os

class RSVPTrainingDataCollection:

    def __init__(self, window, target_image_folder, distract_image_folder,
                 blank_image_path=os.path.join('D:\Workspace','PULSD','PsychoPy-pylsl-RSVP','images','blank','black.png'),
                 trials=4,
                 inter_trial_rest=4,
                 n_images_per_batch=20,
                 rest_after_target_length=8,
                 ms_per_frame=20,
                 ms_stim_flash_dur=250,
                 ms_blank_dur=50):

        self.window

        self.target_image_folder = target_image_folder
        self.distract_image_folder = distract_image_folder
        self.blank_image_path = blank_image_path

        self.trials = trials
        self.inter_trial_rest = inter_trial_rest #seconds

        self.n_images_per_batch = n_images_per_batch
        self.rest_after_target_length = rest_after_target_length #units? frames or stimuli or time?

        self.ms_per_frame = ms_per_frame
        self.ms_stim_flash_dur = ms_stim_flash_dur
        self.ms_blank_dur = ms_blank_dur


    
