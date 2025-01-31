# Smart Camera Parking System (SCPS)

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