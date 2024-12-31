# ShockerSecurity: DIY Security Camera System with Facial Recognition

By: Jacob M & Tina L

## High-level Overview
The core stack for this project was pretty straightforward: the Raspberry Pi, a camera module, and a combination of Python, OpenCV, and Flask. The Raspberry Pi 4 served as the main processing unit, with the camera module capturing video footage. Python, being one of the most accessible programming languages for prototyping (as well as the main recommended language for developing on a Raspberry Pi), made sense for writing scripts to handle the image processing and facial recognition. We used OpenCV for the computer vision side of things, mainly for detecting faces in the camera feed.

Flask was used to build a lightweight web server where users could log in, watch live footage, and manage the database. This part was critical since it allowed authorized users to interact with the system through a simple interface without needing to get their hands dirty in the code. To store the footage, we opted for a SQLite database where each entry contained metadata like the date and time of recording, the faces identified, and whether or not the footage had been flagged. The backend logic, handled by Python, made it easy to update, delete, and flag footage based on facial recognition results.

### Core Components
- **Backend**: Python, OpenCV, Flask, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Hardware**: Raspberry Pi 4, Camera Module 3 NOIR

---

## Backend Development and Implementation

### Setting Up the Flask App
At the heart of this project is a Flask web application. Flask isn’t the most complex web framework, but its simplicity is what makes it perfect for this kind of project—just enough to make your system run smoothly without needing to spend hours navigating through a bloated structure. 

The Flask app is built on several blueprints, each handling a specific function, such as user login, video streaming, and face detection. 

You can view the full implementation of the Flask app [here](https://github.com/jmund15/ShockerSecurity/blob/0161ed6565bb9fbf4d2d56fb28d644db717cb095/backend/flaskApp.py#L1).

---

### Video Capture, Feed, and Facial Recognition
The system continuously captures frames from the camera, which are processed in real time for face detection. When the system detects a face, it compares it to previously stored face data, running through a set of encodings stored in the database.

You can view the full implementation for facial recognition [here](https://github.com/jmund15/ShockerSecurity/blob/0161ed6565bb9fbf4d2d56fb28d644db717cb095/backend/flaskStream.py#L79).

---

### Managing the Database with SQLite
SQLite was used to store user credentials and face data securely. The system allows adding, updating, and deleting face records, with a unique naming system to avoid overwriting existing records.

You can view the full database handling logic [here](https://github.com/jmund15/ShockerSecurity/blob/0161ed6565bb9fbf4d2d56fb28d644db717cb095/backend/SQLiteConnect.py#L1).

---

### User Authentication and Access Control
User authentication is handled using Flask-Login. The login system ensures that only authorized users can access certain parts of the application, such as the live feed and face management sections.

You can find the user authentication code [here](https://github.com/jmund15/ShockerSecurity/blob/0161ed6565bb9fbf4d2d56fb28d644db717cb095/backend/flaskLogin.py#L26).

---

### Email Alerts and Notifications
The system sends email notifications when unauthorized or unidentified faces are detected. The emails include a photo of the person and a link to the live stream.

You can view the email alert implementation [here](https://github.com/jmund15/ShockerSecurity/blob/0161ed6565bb9fbf4d2d56fb28d644db717cb095/backend/sendEmail.py#L1).

---

## Frontend Development and Implementation

### HTML & CSS
The frontend interface is built using HTML, providing the structure for key sections like the Face Management Module and Streaming Module.
CSS was used to style the entire interface, ensuring a clean and user-friendly experience.

---

### JavaScript
JavaScript enables interactivity, such as adding or removing faces from the system and controlling the video stream's functionality.

---

You can find the full frontend structure [here](https://github.com/jmund15/ShockerSecurity/tree/master/frontend).

## Hardware Development and Implementation

### Procuring the Hardware
The hardware setup includes a Raspberry Pi 4B and a Camera Module 3 NOIR, chosen for their compatibility and performance.

---

### The 3D-Printed Case
A custom 3D-printed case was designed to house the Raspberry Pi and camera, providing durability and easy mounting on a door or wall.

---

## Conclusion
This DIY security camera system integrates facial recognition, video streaming, and an intuitive web interface for real-time monitoring. The project involved both software and hardware development, providing a valuable learning experience.

Feel free to explore the code and hardware design through the links above, and contribute if you’d like to improve or extend the system.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

