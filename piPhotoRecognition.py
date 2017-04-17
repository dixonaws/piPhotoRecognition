from picamera import PiCamera
import picamera
from time import sleep
from gpiozero import Button
import datetime as dt
import boto3
import os

camera=PiCamera()
button=Button(17)
frame=1
s3=boto3.client('s3')
rk=boto3.client('rekognition')

camera.annotate_background=picamera.Color("Black")
camera.annotate_foreground=picamera.Color("Yellow")

# our S3 bucket
bucket_name='piphotorecognition'

camera.start_preview()

# enter an infinite loop that is only broken by a KeyboardInterrupt (control+c)
while True:
	try:
		button.wait_for_press()
		timestamp=dt.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')

		camera.annotate_text = "Capturing frame " + str(frame) 

		# establish a name for the file using the timestamp and frame number
		filename="frame" + str(frame) + "-" + timestamp + ".jpg"
		camera.capture(filename)
		camera.annotate_text = "Captured frame " + str(frame) + " (" + timestamp + ")"

		# upload the file to S3
		print("Uploading " + filename + "...")
		s3.upload_file(filename, bucket_name, filename)
		
		# increment the frame variable and delete the file
		frame=frame+1
		os.remove(filename)
	except KeyboardInterrupt:
		camera.stop_preview()
		break




