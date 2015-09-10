import ConfigParser
import os
import pygame
import time
import random
import glob

class pyscope :
    screen = None
    size   = None

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

        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (self.size[0], self.size[1])
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def display(self, image):
        image.scale(self.size[0], self.size[1])

        # Get updated image size
        (iw, ih) = image.get_size()

        dsize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        xp = (dsize[0] - iw) / 2  # find location to center image on screen
        yp = (dsize[1] - ih) / 2

        # Blank the screen incase the image doesn't fill it all
        self.screen.fill([0, 0, 0])
        self.screen.blit(image.handle,(xp,yp))
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
    img_height = None
    img_width = None

    def __init__(self, filename):
        print "hello my name is: {0}".format(filename)
        self.handle = pygame.image.load(filename).convert()
        self.img_height = self.handle.get_height()
        self.img_width  = self.handle.get_width()

    def get_size(self):
        return (self.img_width, self.img_height)

    def scale(self, screen_width, screen_height):
        print "sh: %d  sw: %d" % (screen_height, screen_width)

        # If the image isn't already the same size as the screen, it needs to be scaled
        if ((self.img_height != screen_height) or (self.img_width != screen_width)):
            # Determine what the height will be if we expand the image to fill the whole width
            scaled_height = int((float(screen_width) / self.img_width) * self.img_height)
            print "scaled_height {0}".format(scaled_height)
            # If the scaled image is going to be taller than the screen, then limit the maximum height and scale the width instead
            if (scaled_height > screen_height):
                print "1"
                scaled_height = screen_height
                scaled_width = int((float(screen_height) / self.img_height) * self.img_width)
            else:
                print"2"
                scaled_width = screen_width

            img_bitsize = self.handle.get_bitsize()

            # transform.smoothscale() can only be used for 24-bit and 32-bit images. If this is not a 24-bit or 32-bit
            # image, use transform.scale() instead which will be ugly but at least will work
            if (img_bitsize == 24 or img_bitsize == 32):
                self.handle = pygame.transform.smoothscale(self.handle, (scaled_width, scaled_height))
                print "3 sh: %d  sw: %d" % (scaled_height, scaled_width)
            else:
                self.handle = pygame.transform.scale(self.handle, (scaled_width, scaled_height))
                print "4 sh: %d  sw: %d" % (scaled_height, scaled_width)

            print "oh: %d  ow: %d" % (self.img_height, self.img_width)
            self.img_height = scaled_height
            self.img_width = scaled_width
            print "ih: %d  iw: %d" % (self.img_height, self.img_width)


# ...and begin
config = ConfigParser.ConfigParser()
config.read("./config.ini")
print config.sections()
delay = int(config.get("Common", "delay"))
print "delay %d" % (delay)

scope = pyscope()

for x in range(0,1):

    filetypes = ('./*.PNG', './*.png', './*.JPG', './*.jpg', './*.JPEG', './*.jpeg')
    files_grabbed = []
    for files in filetypes:
        files_grabbed.extend(glob.glob(files))
    files_grabbed.sort()

    print files_grabbed

    for f in files_grabbed:
        i = image(f)
        scope.display(i)
        time.sleep(delay)
