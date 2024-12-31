# ShockerSecurity

## Senior Design II - Engineering Open House Presentation
**Team Members**: Jacob Mund & Tina Leung

---

## Project Overview

**ShockerSecurity** is a compact, cost-efficient, and scalable security system built using a Raspberry Pi 4B with the Pi Camera Module 3 (NOIR). The system features facial recognition capabilities and utilizes a variety of technologies to provide a complete security solution. 

- **System Cost**: < $100
- **Camera**: Pi Camera Module 3 (NOIR) chosen for night-vision capabilities
- **Resolution**: Footage captured at 30fps
- **Main Features**: 
  - Facial identification system with live footage streaming
  - SQLite database for storing user data and faces
  - Email notifications for unauthorized face detection

---

## Features & Code Showcase

### Security System Features

#### 1. **Capturing & Yielding Frames (Main Thread)**
   - The main thread captures and yields frames continuously from the camera module.

#### 2. **Face Identification (Background Thread)**
   - Facial recognition runs in the background to process frames and identify faces.
   - Face annotations are created and displayed when identified.

#### 3. **SQLite Database Integration**
   - **Database**: SQLite is used for storing user accounts and face data.
   - **Read Queries**: Return respective Python class objects.
   - **Write Queries**: Used when new faces are detected or users are registered.

#### 4. **Email Notification System**
   - **Purpose**: Alerts users on unknown or unauthorized face detections.
   - All registered users receive an email with the image of the detected face.

#### 5. **Streaming Module**
   - **Live Streaming**: Security footage is streamed frame-by-frame through an MJPEG stream.
   - Users can access the stream and switch to fullscreen mode.

---

## Feature Showcase

### Database and Email

- **Email Notification**:
  - Notifies users of any unauthorized face detection.
  
- **Database Module Excerpt**:
  - Shows how facial data and user accounts are handled in the SQLite database.

---

### Face Management and UI

- **Face Management**:
  - Users can view, update, and remove faces from the database through a dedicated UI page.
  
- **Live Stream UI**:
  - A user-friendly interface for streaming camera footage in real-time.
  
- **Database Management UI**:
  - A page for managing user face data, including adding and deleting faces.

---

### Authentication and Security

- **Login System**:
  - Implemented a secure login system with hashed passwords stored in the database.
  - CSRF and CORS validation implemented for security.

- **3D-Printed Case**:
  - A custom-designed CAD model to house the ShockerSecurity system.
  - The case features cutouts for cable ports and camera module.
  - The final design is intended to be mounted on a door or window sill.

---

## Feature Showcase: Login and Case

- **User Login UI**:
  - Interface for securely logging into the system.

- **3D-Printed Case**:
  - The 3D-printed case is designed to securely house the system, ensuring protection and portability.

---

## Conclusion

Through the course of this project, we have gained experience and skills in the following areas:
- Project management
- Hardware and software integration
- Full stack development
- Database management
- Facial detection technology
- CAD design and 3D printing
- Team communication and workload delegation

---

## Acknowledgements

Thank you to our professors and mentors for their guidance and support throughout this project. 

Feel free to explore the code and contribute to future improvements!

