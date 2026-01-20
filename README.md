# Ai-Ping-Pong


📌 Project Overview
AI-Vision-Pong is a Python-based application that bridges the gap between physical motion and digital gameplay. By leveraging the OpenCV library, the project implements a real-time object tracking system (MOSSE) that translates the horizontal movement of any physical object into paddle controls for a customized Pong game engine.

🛠 Technical Stack
Language: Python 3.x

Computer Vision: OpenCV (opencv-contrib-python)

Mathematics: NumPy (for coordinate mapping and linear interpolation)

Tracking Algorithm: MOSSE (Minimum Output Sum of Squared Error)

⚙️ Core Mechanics
The system operates on a three-tier architecture:

Vision Layer: Captures and mirrors the webcam feed, processing frames at high FPS.

Tracking Layer: Uses the MOSSE legacy tracker to provide low-latency coordinate data from a user-defined Region of Interest (ROI).

Game Engine: A custom physics loop that handles ball vector math, AI logic, and collision detection.

Coordinate Transformation

To ensure smooth control, the camera's horizontal pixel coordinates are mapped to the game environment using linear interpolation:

x 
game
​	
 =interp(x 
camera
​	
 ,[0,frame_width],[0,game_width])

Install dependencies:

Bash
pip install opencv-contrib-python numpy
Run the application:

Bash
python main.py
🎮 Execution Instructions
Initialization: Upon launch, the system will open a camera feed.

Calibration: Press 'r' to enter ROI selection mode.

Targeting: Click and drag a bounding box over a high-contrast object (e.g., a bright tennis ball, a smartphone, or a colored marker).

Engagement: Press ENTER to lock the tracker. Move the object laterally to control the bottom paddle.

Termination: Press 'q' to safely release system resources and exit.

📈 Optimization Notes
The MOSSE tracker was specifically chosen for this implementation due to its high computational efficiency, making it ideal for real-time gaming where frame-rate consistency is critical. While it is less robust than CSRT to occlusions, it provides the lowest input lag for motion-to-screen translation.
