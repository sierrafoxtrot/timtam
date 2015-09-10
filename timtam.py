import os
import pygame
import time
import random
import glob

class pyscope :
    screen = None;

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

class image :
    handle = None

    def __init__(self, filename):
        name = filename
        print "hello my name is: {0}".format(name)
        self.handle = pygame.image.load(i).convert()

    # The centre of the raw image (unscaled)
    def centre(self):
        isize = self.handle.get_size()
        dsize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        xp = (dsize[0] - isize[0]) / 2  # find location to center image on screen
        yp = (dsize[1] - isize[1]) / 2
        return (xp,yp)

    def scale(self):
        img_height = img.get_height()
        img_width = img.get_width()

        # If the image isn't already the same size as the screen, it needs to be scaled
        if ((img_height != self.screen_height) or (img_width != self.screen_width)):
            # Determine what the height will be if we expand the image to fill the whole width
            scaled_height = int((float(self.screen_width) / img_width) * img_height)

            # If the scaled image is going to be taller than the screen, then limit the maximum height and scale the width instead
            if (scaled_height > self.screen_height):
                scaled_height = self.screen_height
                scaled_width = int((float(self.screen_height) / img_height) * img_width)
            else:
                scaled_width = self.screen_width

                img_bitsize = img.get_bitsize()

                # transform.smoothscale() can only be used for 24-bit and 32-bit images. If this is not a 24-bit or 32-bit
                # image, use transform.scale() instead which will be ugly but at least will work
                if (img_bitsize == 24 or img_bitsize == 32):
                    img = pygame.transform.smoothscale(img, [scaled_width, scaled_height])
                else:
                    img = pygame.transform.scale(img, [scaled_width, scaled_height])

                # Determine where to place the image so it will appear centered on the screen
                display_x = (self.screen_width - scaled_width) / 2
                display_y = (self.screen_height - scaled_height) / 2
        else:
            # No scaling was applied, so image is already full-screen
            display_x = 0
            display_y = 0

    def display(self, scope):
        (xp, yp) = self.centre()
        # Blank the screen incase the image doesn't fill it all
        scope.screen.fill([0, 0, 0])
        scope.screen.blit(self.handle,(xp,yp))
        pygame.display.update()


scope = pyscope()

for x in range(0,1):

    images = glob.glob("./*.jpg")

    print images

    for i in images:
        thingy = image(i)
        error this is arse about. pass image to screen not the other way around.
        thingy.display(scope)
        #time.sleep(2)
