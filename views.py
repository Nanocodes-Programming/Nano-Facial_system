from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from .models import UserProfile
import numpy as np
import cv2
from django.contrib.auth import authenticate, login
from .forms import LoginForm
import time
import os
import io
from django.core.files import File
from .face_capture import capture_and_store_image
import face_recognition
import PIL
# Create your views here.

def login_view(request):
    # Check if the request method is POST
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Get the username from the request
        username = request.POST['username']

        from django.shortcuts import get_object_or_404

        # Get the user object for the given username or raise a 404 error if it does not exist
        user = get_object_or_404(UserProfile, username=username)

        # Get the image associated with the user
        uploaded_image = user.image

        # run face capture nd store image
        face_cascade = cv2.CascadeClassifier(r'FaceUnlock/haarcascade.xml')
        cap = cv2.VideoCapture(0)

        while True:
            # Capture the video frame
            ret, frame = cap.read()
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                # Get the coordinates of the detected face
                x, y, w, h = faces[0]
                # Crop the face from the frame
                face = frame
                # Save the face to a file
                cv2.imwrite(r'media/FaceRegImages/capture.jpg', face)
                break
            # Release the video capture
            cap.release()
            # Destroy the window
            cv2.destroyAllWindows()

            # Read the captured image
            captured_image = cv2.imread(r'media/FaceRegImages/capture.jpg')
            # Convert the image to a numpy array
            image_array = np.fromstring(captured_image, np.uint8)
            # Convert the numpy array to a cv2 image
            image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
            user.save()

            # Facial Recognition System
        known_image = face_recognition.load_image_file(uploaded_image)
        unknown_image = face_recognition.load_image_file(r'media/FaceRegImages/capture.jpg')

        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        if results:
                 # If the images are a match, authenticate and login the user
            user = authenticate(request, username=username)
            if request.user.is_authenticated:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Authentication Failed!!")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form and create a new user
            username = form.cleaned_data['username']
            image = form.cleaned_data['image']
            user = UserProfile.objects.create(username=username, image=image)

            # Redirect the user to the login page
            return redirect('login')
    else:
        form = SignupForm()
    context = {
        'form': form,
        'user' : request.user
    }
    return render(request, 'signup.html', context)



def home(request):
    user = UserProfile.objects.all()
    return render(request, 'index.html', {'user':user})
