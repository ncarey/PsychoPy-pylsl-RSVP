from psychopy import visual, core, event
import pylsl
import os

class RSVPPy:

    #deprecated
    def process(self, image_path):
                
        do_not_break = True
        while do_not_break: 
            for cur_img_index in range(1, self.n_images_per_batch + 1):
                self.images[cur_img_index-1].draw()
                self.window.flip(clearBuffer=True)
                #Qmywin.callOnFlip(sendMarker, outlet=m_outlet, img_index=cur_img_index)
                
                if len(event.getKeys())>0:
                    do_not_break=False
                event.clearEvents()
                
        self.window.close()
        core.quit()

    def presentImageBatch(self):
        #magic nums for now. We want a flash duration of 250ms, with blank screen for 50ms
        #however we are working in frames, not ms
        #so, we want frame_flash_dur = 250 / ms_per_frame

        ms_flash_dur = 250
        ms_blank_dur = 50

        frame_flash_dur = int(ms_flash_dur / self.ms_per_frame)
        frame_blank_dur = int(ms_blank_dur / self.ms_per_frame)

        for cur_img_index in range(1, self.n_images_per_batch + 1):
            #present one image
            for cur_frame in range(frame_flash_dur + frame_blank_dur):
                if cur_frame < frame_flash_dur:
                    #draw pic, if cur frame is 1 then callOnFlip for stim/trigger sending
                    self.images[cur_img_index-1].draw()
                else:
                    #draw black
                    self.black_image.draw()
                self.window.flip()

        
                    

    def loadCurrentImages(self):

        #clear image array
        self.images = []
        #repopulate
        for cur_img_index in range(1, self.n_images_per_batch + 1):
            image_name = "{num:02d}.png".format(num=cur_img_index)
            image_path = os.path.join(self.image_buffer_path, image_name)
            self.images.append(visual.ImageStim(win=self.window, image=image_path, name=image_name))

        
    def __init__(self, window, image_buffer_path, ms_per_frame, images_per_batch=20):

        self.window = window
        self.images = []
        self.n_images_per_batch = images_per_batch
        if(self.n_images_per_batch > 99):
            print("Error, currently we only support up to 99 images per batch")
            exit()
            
        self.image_buffer_path = image_buffer_path
        self.ms_per_frame = ms_per_frame

        black_path = os.path.join(self.image_buffer_path, '../black.png')
        self.black_image = visual.ImageStim(win=self.window, image=black_path, name='black')
            
if __name__=='__main__':


    win = visual.Window([800,600],monitor="ASUSLaptopMonitor", units="deg", checkTiming=True)
    print("Estimated Frame Duration: {0}".format(win.monitorFramePeriod))
    cur_ms_per_frame = win.getMsPerFrame(nFrames=300, msg='Assessing Frame Rate...')
    print("Estimated ms per Frame: Avg: {0} Standard Dev: {1}, Median: {2}".format(cur_ms_per_frame[0], cur_ms_per_frame[1], cur_ms_per_frame[2]))                      
    image_p = os.path.join('D:\Workspace\PULSD\OpenVibe-HiddenCube', 'buffers\CurrentImages')


    rsvp = RSVPPy(win, image_buffer_path = image_p, images_per_batch = 20, ms_per_frame = cur_ms_per_frame[2])
    rsvp.loadCurrentImages()
    rsvp.presentImageBatch()
    
