# Cloud_Computing
Repo for all the code from my Cloud Computing project. The Python-Flask front end application, the Cloud Functions deployed on GKE, and the Google Cloud SQL RESTful interactions.
It was essentially a video streaming application, where users could upload videos to our platform and then stream them from the cloud on any device. The application was built from scratch using Python, HTML, CSS, JavaScript and used the Flask framework. 
The front end of the application would make RESTful API calls to the Cloud Functions hosted on Google Functions which would interact with the backend Cloud MySQL table to reurn a JSON reponse, which would be parsed by the front-end and displayed to the user. 
- I developed this project for my Cloud Computing class CSE 5333 under Dr. Habeeb Olfuwobi. 
- I've used Python Flask to build the front end of the web application and deployed them on GCP on their Google App Engine. 
- Wrote multiple API's using Python and hosted them on Google Cloud Functions. Used Google Cloud MySQL to store relational data and interacted with from the Cloud Functions. 
- Also made the front end interact with Google Cloud Storage to access stored images and video, to stream on the go. 
