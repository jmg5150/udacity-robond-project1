[//]: # (Image References)
[image_0]: ./misc/rover_image.jpg
[![Udacity - Robotics NanoDegree Program](https://s3-us-west-1.amazonaws.com/udacity-robotics/Extra+Images/RoboND_flag.png)](https://www.udacity.com/robotics)
# Search and Sample Return Project


![alt text][image_0]

## This repository contains my solution to Project 1 / Search and Sample Return for the Udacity Robotics Software Engineering Nanodegree. The base repository for this project can be found [here](https://github.com/udacity/RoboND-Rover-Project)


## Performance Summary
I recorded videos of two trial runs and uploaded them to YouTube for easy viewing:
[Trial #1](https://youtu.be/wdaQHUwA1lo)
[Trial #2](https://youtu.be/oprh2u0FQSQ)

| Trial # | Mapped % | Fidelity % | Located Rocks | Collected Rocks | Runtime | 
|---------|----------|------------|---------------|-----------------|---------|
| 1       | 54.7%    | 79.4%      | 1             | 1               | 254.4s  |
| 2       | 41.1%    | 70.0%	  | 2			  | 2               | 274.4s  |


The required project writeup contains additional details regarding the implementation and performance and can be viewed [here](/writeup.md)

## Remarks
I developed the code to optomize for highest fidelity as the highest priority, as such, the speed of the rover is relatively slow. I am rather satisfied with my implementation of finding rocks and picking them up once they are within the field of view, however I think there could be much improvement in the overall navigation of the rover. One particular shortcoming in the code is that there is no method to guide the rover into searching undiscovered areas vs. going through areas on the map it has already explored.


