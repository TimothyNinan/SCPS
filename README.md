# Smart Camera Parking System (SCPS)

## Summary
The Smart Camera Parking System is a modern solution designed to transform traditional parking management into a fully digital, autonomous process. By combining license plate recognition technology with a user-friendly web interface, this system automates vehicle registration, parking duration tracking, and payment processing. It eliminates the need for manual ticketing, addressing the growing demand for efficient, secure, and streamlined parking solutions while improving the overall user experience.
The need for modernization arises from the increasing demand for parking systems that are fast, reliable, and secure. The Smart Camera Parking System meets these needs by providing a dependable, automated method for reading license plates. This innovation enhances parking facility management and ensures seamless user interactions.
The development process faced significant technical challenges, including accurate license plate recognition, efficient image processing using AI models and Optical Character Recognition (OCR), secure storage and management of user data, and seamless integration of hardware and software. Overcoming these challenges required a sophisticated approach that combined embedded systems hardware with advanced software algorithms, ensuring high performance and reliability in real-world scenarios.
The system autonomously reads license plates at parking facility entrances and exits, logs vehicle entry and exit times, calculates parking duration, and displays charges to users. Key components include a Raspberry Pi for processing, a camera module for image capture, and a web interface for user interaction. A 3D-printed housing encloses the hardware, providing durability and protection, while a power bank supports portable and consistent operation.
The system achieved a 95% accuracy rate in license plate recognition during testing, a critical metric for ensuring reliability and building user trust.
The final product is a tripod-mounted device equipped with a camera, Raspberry Pi, and battery, integrated with a web-based interface for managing parking details and payment options. This prototype demonstrates the feasibility of the solution and highlights its potential to improve real-world parking experiences.
Future developments will include features like a navigation monitor to guide vehicles within parking garages, providing a complete end-to-end solution for modern parking management. These enhancements will build on the current design, addressing broader needs in parking and traffic management systems while paving the way for widespread adoption.

### Diagrams

## Images



## Setup

### Download the Files

Clone the repository:

``` 
git clone https://github.com/TimothyNinan/SCPS.git
```

### Install Requirements

Inside the scpstApp directory, follow the below steps.

1. Create a virtual environment:

``` 
python3 -m venv venv
```

2. Activate the virtual environment:

``` 
source venv/bin/activate
```

3. Install the requirements:

``` 
pip install -r requirements.txt
```

### Run the App 

In the virtual environment, in the scpstApp directory, run the app:

``` 
python app.py
```

The Flask App should be started (takes around 20 seconds). 

Navigate to [127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to see the user side of the app.


#### Run the Model

Navigate to [127.0.0.1:5000/admin](http://127.0.0.1:5000/admin) in your browser to see the admin side of the app.

Upload an image to the GCP Bucket manually or wait for the pi to upload an image.

Click the "Start Model" button to start the model. After the timer completes (every 30 seconds) the model will run automatically. It will give you the results of the OCR (non-parsed). On the side, the users list will be updated with a new blank user with the license plate (OCR-parsed).

The model will continue to run every 30 seconds. Click the "Stop Model" button to stop the continuous execution.