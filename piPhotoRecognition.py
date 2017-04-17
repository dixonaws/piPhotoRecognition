from picamera import PiCamera
import picamera
from time import sleep
from gpiozero import Button
import datetime as dt
import boto3

camera=PiCamera()
button=Button(17)
frame=1
s3=boto3.client('s3')
rk=boto3.client('rekognition')

camera.annotate_background=picamera.Color("Black")
camera.annotate_foreground=picamera.Color("Yellow")
bucket_name='piphotorecognition'

camera.start_preview()

while True:
	try:
		button.wait_for_press()
		timestamp=dt.datetime.now().strftime('%m-%d-%Y-%H:%M:%S')

		camera.annotate_text = "Capturing frame " + str(frame) 
		filename="frame" + str(frame) + "-" + timestamp + ".jpg"
		#filename="frame" + str(frame) + ".jpg"
		camera.capture(filename)
		camera.annotate_text = "Captured frame " + str(frame) + " (" + timestamp + ")"

		print("Uploading " + filename + "...")
		s3.upload_file(filename, bucket_name, filename)
		
		frame=frame+1
	except KeyboardInterrupt:
		camera.stop_preview()
		break




