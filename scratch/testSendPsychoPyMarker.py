from psychopy import visual, core, event #import some libraries from PsychoPy
import os
from pylsl import StreamInfo, StreamOutlet


info = StreamInfo(name='test_stream', type='Markers', channel_count=1, channel_format='int32', source_id='psychopyStimuli')
m_outlet = StreamOutlet(info)


def sendMarker(outlet, img_index):
    outlet.push_sample(x=[img_index])

#image path
project_dir = 'D:\Workspace\PULSD\OpenVibe-HiddenCube'
image_dir = os.path.join(project_dir, 'buffers','CurrentImages')

#create a window
mywin = visual.Window([800,600],monitor="testMonitor", units="deg", checkTiming=True)
print("Estimated Frame Duration: {0}".format(mywin.monitorFramePeriod))

images = []

for cur_img_index in range(1,21):
    image_name = "{num:02d}.png".format(num=cur_img_index)
    image_path = os.path.join(image_dir, image_name)
    images.append(visual.ImageStim(win=mywin, image=image_path, name=image_name))

#draw the stimuli and update the window
do_not_break=True
while do_not_break: #this creates a never-ending loop
    for cur_img_index in range(1,21):
        images[cur_img_index-1].draw()
        mywin.flip()
        mywin.callOnFlip(sendMarker, outlet=m_outlet, img_index=cur_img_index)
    
        if len(event.getKeys())>0:
            do_not_break=False
        event.clearEvents()

#cleanup
mywin.close()
core.quit()