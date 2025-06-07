[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/NJLWAR4a)

![Docs Added](https://github.com/edl-iitb/edl-25-project-submission-edl25_mon16/actions/workflows/classroom.yml/badge.svg)

<!-- DON'T MODIFY ANYTHING ABOVE -->

<!-- Modify from here -->
# MIRAGE - Motion Integrated Real Time Articulated Glove Emulator
This document serves as a comprehensive guide for the project submission. 
## Project Overview
The project is a portable, wearable, exoskeleton glove. The glove, once worn, is able to detect the motions of the hand and simulate the motion on Unity on our Laptop. The exoskeleton glove is 3d printed, and each finger joint has a rotary encoder in it, which is used to figure out the amount of rotation. 
### Project Name: Exoskeleton glove for sensing precise hand movements
### Team Number: Mon-16
### Team Members:
- Nishant Bhave   (22B2144)
- Prajwal Nayak   (22B4246)
- Reeyansh Shah   (22B0412)
- Shikhar Moondra (22B0688)
- Siddick Khatri  (22B4241)

### Problem Statement and Solution:
The problem statement was to build a sensing exoskeleton glove to measure precise movements of fingers. The exoskeleton glove has to sense precise angular movement of each of the joints of the finger. It needs to transmit the captured data to a laptop which will recreate this movement using a 3D hand simulation. We were expected to deliver a functional exeskeleton glove which can be worn by a user and a 3D simulated model which tracks the user's hand movements using the exoskeleton glove. Some other expectations are as follows:
- Should be able to measure 1 degree angular movements of each finger joint
- Should be able to recreate the simluated movement within 1 second lag
- Should be battery operated for atleast half hour.

We solved this problem in the following ways:
- We made a exoskeleton glove (3D printed whose files are in the 3D_models subdirectory), which has spaces to attach rotatry encoders in them and they bend enough to get a precise measurement of the bending of the joints. The rotary encoders are basically potentiometers where the angle rotated is proportional to the angle rotated given that the angle lies in the range 0 to 2 pi. 
- The readings of the encoders are read by the raspberry pi pico w (which has an inbuilt Wifi module) as values from 0 to 65536 (16 bit). These values are sent to the Printed Circuit Board (whose schematic is given in the pcb subdirectory).
- The PCB mainly has 2 multiplexers and the Raspberry pi pico W mounted on it. It has header pins for taking in the values of the encoders. The multiplexers, based on the select pin values given by the Rpi, select which rotary encoders to read. The outputs of the multiplexers are connected to the ADC pins on the Rpi. The Rpi takes these readings and sends it to the laptop wirelessly using the UDP protocol. The Rpi code was written on Thonny which I have uploaded on the /src/Rpi_code folder.
- The values sent by Rpi are recieved by a python code running on the PC which then does some slight filtering/smoothening and forwards the value to the app (designed by unity).
- The app has a rigged hand model (which was designed on blender whose design is in the others folder). It also has the code for recieving values and converting it to angles and showing the intended fingers  bending. There are two sets of calibration post which the hand starts making accurate movements (code on /src/unity_codes).

We having worked on developing an exoskeleton glove, which involved circuit design, sensor integration, and mechanical assembly.We as a team learnt a lot of technical skills from this project : 3D Modelling, Raspberry pi coding on Thonny, using multiplexers, designing PCBs, using blender, and unity (C#), wiresless transmission of data using UDP protocol This experience significantly enhanced our skills in time management, teamwork, and collaboration. We faced several challenges, particularly during PCB fabrication, which taught us the importance of early planning and maintaining buffer time to manage unforeseen delays. Working late into the night became common as we strived to meet deadlines while maintaining accuracy. We learned to divide tasks effectively, communicate clearly, and support each other through technical and logistical hurdles. A key takeaway was the ability to balance seeking guidance when necessary with independently troubleshooting problems. Overall, it was a comprehensive learning experience that combined technical rigor with essential project management and interpersonal skills.

Due to time constraints and some last minute issues of raspberry pi heating up, we were not able to power the exoskeleton glove with the battery and decided to power it using our PC instead. Nevertheless the transmission is still over wifi setup using our hotspot. We look forward to debug this issue rigorously and make the glove operational using a battery for portable deployability. The Glove has immense application in rehabilitation and VR gaming industry and although we attempt to show its functioning though the prosthetic arm, we are excited to implement this project on a standard pneumatic actuated glove to help out and do our bit for the society!

## 1. Source Code

All source code files are organized under the `/src` directory. Each subdirectory has clear descriptions about their purpose and functionality. Every subfolder has a README.MD file which explains the purpose of the code and all the commands used.

### Folder Structure:
```plaintext
/Project-Root 
├── /src 
  ├── /Rpi_code
     ├── rpi.py
  ├── /python-code
     ├── python.py
  ├── /unity_codes
     ├── /handcontroller
        ├── /Hand_control.cs
     ├── /camera_rotation
        ├── /CameraOrbit.cs
```

## 2. PCB Design

The project involves designing a printed circuit board (PCB). We have provided the design files in the `/pcb` folder. The PCB was designed using KiCAD. The picture of our final PCB Layout is present under the `/pcb/<PCB_X>/pictures` folder.

### Folder Structure:
```plaintext
/Project-Root 
├── /pcb 
  ├── /PCB1
    ├──/pictures
      ├──3D view.png
      ├──PCB layout.png
      ├──circuit.png
    ├── PCB.kicad_pcb 
    ├── pcb.kicad_sch
```
---

## 3. 3D Models
The project includes 3D models that require 3D printing. The files are placed in the `/3d_models` directory. Create separate subfolders for different models and provide a description of the design process and tools used.

### Folder Structure:
```plaintext
/Project-Root
├── /3d_models
  ├── /Exoskeleton Glove
     ├── Rot Pot V1.jpg
     ├── Rot Pot v1.stl
     ├── connect 1.jpg
     ├── connect 1.stl
     ├── connect 2.stl
     ├── connect base.jpg
     ├── connect base.stl
     ├── connect2.jpg
     ├── index sensor place 1 velcro v12.jpg
     ├── index sensor place 1 velcro v12.stl
     ├── palm base v1.jpg
     ├── palm base v1.stl
     ├── pcb case easy v1.jpg
     ├── pcb case easy v1.stl
     ├── pcb case top v1.jpg
     ├── pcb case top v1.stl
     ├── sensor body attachment back v13.jpg
     ├── sensor body attachment back v13.stl
     ├── sensor body attachment base v10.jpg
     ├── sensor body attachment base v10.stl
     ├── sensor body attachment v14.jpg
     └── sensor body attachment v14.stl
  ├── /Prosthetic Arm
     ├── Arm_Cover.jpg
     ├── Arm_Cover.stl
     ├── Assemble_Prosthetic_Arm.png
     ├── Finger_Index.jpg
     ├── Finger_Index.stl
     ├── Finger_Middle.jpg
     ├── Finger_Middle.stl
     ├── Finger_Pinky.jpg
     ├── Finger_Pinky.stl
     ├── Finger_Ring.jpg
     ├── Finger_Ring.stl
     ├── Finger_Thumb.jpg
     ├── Finger_Thumb.stl
     ├── Right_Hand.jpg
     ├── Right_Hand.stl
     ├── arm servo placement v1.jpg
     └── arm servo placement v1.stl

```
---

## 4. Bill of Materials (BOM)

A complete Bill of Materials (BOM) listing of all the hardware components used in the project is provided in this file including both parts obtained from the lab and parts ordered from external vendors or purchased locally.

### Folder Structure:
```plaintext
/Project-Root 
├── bom.xlsx
```
---

## 5. Reports and Presentations

The project presentation and reports include a brief overview of your project, objectives, design process, results, and conclusions. This should include all the milestone submission presentations.

### Folder Structure:
```plaintext
/Project-Root
  ├── /reports 
    ├── Milestone 0 P-12 MON-16.pdf
    ├── Milestone 1 P-12 MON-16.pdf
    ├── Milestone 2 P-12 MON-16.pdf
    ├── Milestone 3 P-12 MON-16.pdf
    ├── Milestone 4 P-12 MON-16.pdf
```

## 6. Other Documents
This directory consists of the Circuit digrams used, making video and the final prototype images of our poject.
### Folder Structure:
```plaintext
/Others
  ├── Circuit Diagram Prosthetic Arm.pdf.jpg
  ├── Circuit_Diagram_Exoskeleton_Glove.pdf
  ├── Making Video.mp4
  ├── Prototype Exoskeleton Glove.jpg
  ├── Prototype Prosthetic Arm.png
  └── Wiring image of Exoskeleton Glove.jpg
```

---
