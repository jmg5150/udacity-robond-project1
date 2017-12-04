## Project #1: Search and Sample Return
Project submission for the Udacity Robotics Software Engineer Nanodegree
Jonathan Georgino

---

### This project writeup is based on the sample template provided in the base repo provided by Udacity.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)
[image3]: ./output/trial1results.jpg 
[image4]: ./output/trial2results.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

This document is intended to fullfil the requirement of the Writeup / Readme.

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

My version of the Jupyter Notebook can be found [here](./code/Rover_Project_Test_Notebook_Jonathan.ipynb).

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

Please see above for the link to the updated Jupyter Notebook for this project. The `process_image()` function has been updated to draw the worldmap using the simulation data that I recorded in the Unity RoverSim application. 

The video of the results can be seen [here](./output/test_mapping_jonathan.mp4).

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

Before discussing the implementation of 'perception_step()', I'd like to first present an additional function that I added to the 'perception.py' file to help improve my solution. This additional function implements a method to perform color thresholding on a given range, instead of just a single cutoff point as in the original 'color_thresh()' function.

```python
def color_thresh_range(img, rgb_thresh_low=(130, 110, 0), rgb_thresh_high=(210, 180, 40)):

    color_select = np.zeros_like(img[:,:,0])

    within_thresh = (img[:,:,0] > rgb_thresh_low[0]) & (img[:,:,1] > rgb_thresh_low[1]) & (img[:,:,2] > rgb_thresh_low[2]) & (img[:,:,0] < rgb_thresh_high[0]) & (img[:,:,1] < rgb_thresh_high[1]) & (img[:,:,2] < rgb_thresh_high[2])
    
    color_select[within_thresh] = 1
    return color_select
```

As you'll see later down the page, I use this function to aid in the detection of rocks. 

That said, now let's walk through my implementation of the 'perception_step()' function. Rather than duplicate the entire code here, I will just be showing interesting snippets and referencing line numbers from within the 'perception.py' file.

A modification I added late in the development of this function, but which comes at the very beginning of the function is to take a look at the 'Rover.pitch' and 'Rover.roll' readings. This can be found on lines 103 - 108.

```python
    valid_cam_img = True
    # 0) Image is really only valid if roll and pitch are ~0
    if Rover.pitch > 0.25 and Rover.pitch < 359.75:
        rvalid_cam_img = False
    elif Rover.roll > 0.75 and Rover.roll < 359.25:
        valid_cam_img = False
```

 The further these values deviate from 0.0, the more innacuracies will make their way into the map, as the output of the perspective transform will be off. As such, I've put thresholds on these parameters, and if they exceed the thresholds, then 'valid_cam_img' will be marked as false. The image is still processed in order to make decisions impacting the rover driving, however the data from that frame is not used to update the map. This prevents the robot from driving blind or zombie-like when roll or pitch is outside the thresholds, but also helps to keep the fidelity of the map high.

 Moving on, I didn't do anything special for steps #1 and #2 of the function template. That code is more or less the boilerplate, whereas I did experiment with some of the values for 'dst_size' and 'bottom_offset', although it did not appear to make much difference in overall performance. The next noticeable modification to my implementation came in step #3, which is where color thresholding is applied to identify navigable terrain/obstacles/rock samples.

 Line 129 shows my use of the above-mentioned 'color_thresh_range()' function.

```python
 rock_cam_view = color_thresh_range(warped_cam_view, rgb_thresh_low=(130, 110, 0), rgb_thresh_high=(210, 180, 40))
```

Steps #4, #5, and #6 are implemented as one would expect given the functions and techniques already presented in the lesson. However, at Step #7 I implemented a technique that I saw presented in the project walkthrough video that I thought was a pretty useful idea. This is due to the distortion that occurs when the image goes through the transformation because the rocks are not flat objects. The follow code corrects for that, and can be found on Lines 152 - 162.

```python
    # Per the Walkthrough video, best to compensate for the actual location of the rocks which is lost during transformation
    if rock_cam_view.any():

        rock_distance, rock_angle = to_polar_coords(rock_xpix, rock_ypix)
        rock_index = np.argmin(rock_distance)
        rock_x_center = rock_x_world[rock_index]
        rock_y_center = rock_y_world[rock_index]
        Rover.rock_angle = rock_angle
        Rover.rock_dist = rock_distance
    else:
        Rover.rock_angle = None
        Rover.rock_dist = None
```


There's just one more thing worthy of explanation in this function, and that can be found on lines 171 - 177.
```python
    if valid_cam_img:
        Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 5

        if rock_cam_view.any():
            Rover.worldmap[rock_y_center, rock_x_center, 1] += 255

        Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 50
```

Here you can see that I finally act on the value stored in 'valid_cam_img' that we set in the very beginning of this function. This only updates the rover's worldmap if pitch and roll are within the threshold I set.

That's it for the 'perception.py' file part of the project. Next I'll be going through the 'deception.py' file and the interesting changes I made there. I must admit that I did a rather poor job of documenting my modifications of this file during the actual project, and now I am trying to remember my thought process a week later. There are two noticeable changes I made to this function. The first one is to change the 'Rover.steer' angle from the mean angle of navigable terrain to the median angle of the terrain. This can be found on line 48.

```python
Rover.steer = np.clip(np.median(target_angle * 180/np.pi)-steering_noise, -15, 15)
```

This is useful when there is an obstacle straight ahead and equal amount of navigable terrain on either side of it, such as the rocks in the center junction / origin of the map in the mission simulator. When using the mean, it's common that the rover drives directly into the obstacles and becomes stuck, however, by using the median, it ensures that the rover steers itself towards an area of navigable terrain which is actually within the dataset. Within that line, you'll also see that I created a variable called 'steering_noise'. I use this to provide an offset to the target angle when we are exploring the map, however once a rock as been found, I set 'steering_noise' to zero so that it drives directly toward the rock. My original intention to offset the steering angle with '-steering_noise' was to bias the rover to a particular side of the path rather than go down the center to aid in map discovery. In the end, I am not sure how helpfup this has been. I could have spent more time characterizing it's impact.

The second noticeable change to this function was to add support for driving towards rock samples once they were located, and then collecting the sample once the rover got within range. The code on lines 39 - 48 shows how the rover would decide to switch from driving towards navigable terrain to driving towards the center point of a located rock sample.
```python
if Rover.rock_angle is not None:
    target_angle = Rover.rock_angle
    steering_noise = 0
    Rover.stop_forward = 50
else:
    target_angle = Rover.nav_angles
    steering_noise = 2
    Rover.stop_forward = 200

Rover.steer = np.clip(np.median(target_angle * 180/np.pi)-steering_noise, -15, 15)
 ```

Essentially, once an angle to a rock sample is found, it takes precedence over the 'nav_angles' of the navigable terrain data. I also lower the threshold for forward stopping so that the rover can get closer to the walls of the path in order to be able to pick up the rock sample. As mentioned above, I do not introduce any steering noise / offset when approaching a rock sample.

Finally, near the bottom of the function, I've added/modified a few lines of code to give the rover a suitable behavior to pick up the rock sample and then transition back to exploration of the map. This can be seen in lines 97 - 104.

```python
# If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
        Rover.stop_forward = 200
        Rover.mode = 'backup'
    elif Rover.near_sample and not Rover.picking_up:
        Rover.throttle = 0
        Rover.brake = Rover.brake_set
        Rover.steer = 0
```

This code makes the rover come to a complete stop once it's close enough to the rock sample to collect it, and then it also provides for sending the command to the collect the rock sample. This also sets 'Rover.mode' to backup so that after it retrieves the sample, it attempts to go backwards. Regrettably I haven't done so much testing and analysis of this particular part of the implementation, so I am unable to jusitfy it's usage with data, however it seems to perform satisfactorily based on observation.

That's pretty much all of the interest things that I've modified or added to these two critical files.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

The Rover Simulator was configured for 1024 x 768 [windowed] resolution with graphics quality set to 'Good'. The development and testing was done on a laptop running Windows 10 (64bit) with 8GB RAM / Intel i7 @ 2.6GHz with Nvidia Gefore GTX 950M GPU.

I recorded videos of two trial runs and uploaded them to YouTube for easy viewing:

[Trial #1](https://youtu.be/wdaQHUwA1lo)

[Trial #2](https://youtu.be/oprh2u0FQSQ)

| Trial # | Mapped % | Fidelity % | Located Rocks | Collected Rocks | Runtime | 
|---------|----------|------------|---------------|-----------------|---------|
| 1       | 54.7%    | 79.4%      | 1             | 1               | 254.4s  |
| 2       | 41.1%    | 70.0%	  | 2			  | 2               | 274.4s  |

![Trial #1 Results][image3] ![Trial #2 Results][image4]

The results in both recorded test runs (and many other non-recorded runs) appear to be above and beyond the minimum performance requirements, however there is still a moderate amount of room for improvement. My approach was to optomize for highest fidelity, which came at a cost of reduced rover speed. Very early on in development, I noticied that slowing the rover down noticeably improved the fidelity of the mapping. I am sure that additional development effort could increase the rover's speed while maintaining satisfactory performance. However, since there were given performance targets for mapping % and fidelity %, but no time requirement, I decided that timing would receive the lowest priority in my development on this project.

While not a hard requirement for this project, it would be underachieving to have a robot capable of picking up rocks and not make an effort to collect the rocks. I am rather pleased with the performance of my implementation - it's able to collect rocks that are located with a ~80% success. One big area of improvement would be to find a better implementation for the rover after a rock has been collected. In most cases, it is pointed almost directly into the wall / obstacle, and since the rover has a very high turning radius, in many cases, it is unable to make the turn that it wants to make in order to get back to navigable space. A more intelligent approach would probably be to backup several meters and return to it's previous orientation before the rock was identified, and then continue on the exploration. This is not something that I chose to implement at this time.

Lastly, one item that I'd like to highlight in my implementation was my decision to have the robot navigate towards the median angle of the navigable terrain instead of the average angle. I noticed that going for the median greatly reduced the amount of times that the robot would get stuck on obstacles in the environment. It also makes complete sense to target the median angle, since there is no certainty that the average angle is actually a valid heading for navigable terrain, whereas, by definition, the median angle is at least a angle that exists in the perceived navigable terrain data set.







