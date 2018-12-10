from psychopy import visual, core, event #import some libraries from PsychoPy
import numpy as np

#create a window
mywin = visual.Window([1920,1080],monitor="testMonitor", units="norm", checkTiming=True)
print("Estimated Frame Duration: {0}".format(mywin.monitorFramePeriod))

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



#create some stimuli
grating = visual.GratingStim(win=mywin, tex=checkTex, size=1.5, pos=[0,0])

#draw the stimuli and update the window
while True: #this creates a never-ending loop
    grating.contrast = grating.contrast * -1
    grating.draw()
    mywin.flip()

    if len(event.getKeys())>0:
        break
    event.clearEvents()

#cleanup
mywin.close()
core.quit()
