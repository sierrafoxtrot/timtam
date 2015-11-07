# What is timtam?

It's a simple program that will display a series of image files on the framebuffer filling the screen as best as possible.

So.... it's a photo frame? Yes.

# What was the itch that timtam originally scratched?

The generic itch was that I needed to display a slideshow at remote locations. Each location had a reasonably large flat panel display. With the addition of a Raspberry Pi, a network connection and a cron job to run rsync (to update the images) the system was running.

The specific requirements (in case they are of interest to anyone else) are that I need the slideshow to be easily updated by muggles. This was achieved by mounting a samba shared drive (that they could easily update). The slideshow display had to be able to handle sporadic updates and periods with zero images in the case where someone deletes all the images before copying the new ones. All the install details are included below.



# How does it work?

PyGame does all the heavy lifting. It really is pretty awesome.



# Does it only work on the Raspberry Pi?

No. Pretty much any platform that supports PyGame should be fine. I chose the Pi because of price and easy availability (ok, it was mostly price).


# Config file options

### delay = [integer number of seconds.]

Default: 5 seconds

Override the default inter-image delay time.

Example:
````
delay = 2
````

### image_directory = [valid pathname]
Default: pwd

Specify the location for image files. Images are pulled from the immediate directory, no recursive search is found.

Example:
````
image_directory = /home/timtam/images
````

### sort = [True/False]
Default: False

If true, the discovered files will be shown in alphabetical order. By default, they are displayed in the order in which they are found.

Example:
````
sort = True
````

### no\_images_msg = [string]

Default: "No Images to show."

A message to display in the event of no images being found in the specified or default locations.

Example:
````
no\_images_msg = "Image directory is empty"
````

### duration\_in_filename = [True/False]

Default: False

If set to True, the display time for an image may be encoded into the filename itself by enclosing it in parenthesis.

Examples (when duration\_in_filename = True)

Filename        | Duration
--------------- | ------------------------------------------
Slide1(12).png  | 12 seconds.
Image(6)(3).jpg | 3 seconds.
Picture.jpg     | default delay period.
shot6.png       | default delay period.



# Notes (Raspberry Pi specific):

## Raspbian (Jessie)

Cancel the GUI and login to a bash prompt
1. Run `sudo raspi-config`
2. Select `3 Boot Options`
3. Select `B2 Text console, automatically logged in a 'pi' user`

4. Then add the following to /home/pi/.bashrc

`cd <timtam_install_dir> ; ./timtam`

5. Then... reboot


## Raspbian (pre-Jessie)

- Needed to enable 32 bit depth on the framebuffer for the raspi:
1. Append `bcm2708_fb.fbdepth=32` to /boot/cmdline.txt (should be possible by config.txt)
2. Add `framebuffer_ignore_alpha=1` to /boot/config.txt

(If on console, the pi user can run the timtam program. Otherwise, needs to be root.)

## How to automatically login to Raspberry Pi text console as pi user.

Step 1: Open a terminal session and edit inittab file.

`sudo nano /etc/inittab`

Step 2: To disable the getty program, navigate to the following line in inittab

`1:2345:respawn:/sbin/getty 115200 tty1`

And add a # at the beginning of the line to comment it out

`#1:2345:respawn:/sbin/getty 115200 tty1`

Step 3: Add login program to inittab.
Add the following line just below the commented line

`1:2345:respawn:/bin/login -f pi tty1 </dev/tty1 >/dev/tty1 2>&1`

This will run the login program with pi user and without any authentication

Step 4: Save and Exit.
Press Ctrl+X to exit nano editor followed by Y to save the file and then press Enter to confirm the filename.

Reboot the pi and it will boot straight on to the shell prompt pi@raspberrypi without prompting you to enter username or password. But this isn't enough; you need your Pi to automatically run some command or a script. which is explained in the next section.

## Run a Script after login

How to automatically run a script after login.
Step 1: Open a terminal session and edit the file /etc/profile

`sudo nano /etc/profile`

Step 2: Add the following line to the end of the file

`. /home/pi/your_script_name.sh`

replace the script name and path with correct name and path of your start-up script.

Step 3: Save and Exit

Press Ctrl+X to exit nano editor followed by Y to save the file.


Scott Finneran (SierraFoxtrot)
scottfinneran+githubATgmailDOTcom
