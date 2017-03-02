# bachelor
Computer vision &amp; path planning
# this is supposed to work now 15/2 -20:36

#Uploaded 23/2-2017
This script includes functions for finding colors and getting info from images.
This is still a working script.

#Version 1
The code searches for the green corners and crop the picture acordingly from the center of the green objects.
It also searches for the red objects within the image, and blacks everything else. Then the objects are made white.
Now the integers representing white (255) is changed to 9 and the image is saved as an matrix in a .txt file. 
The last bit is done to make it easier to retrieve the digits later in c++
