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
# Create your views here.




# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Get the image and username from the form
#             image = form.cleaned_data['image']
#             username = form.cleaned_data['username']

#             # Read the image with cv2
#             image_data = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)

#             # Compare the image with the previously uploaded image for the same user
#             # If the images are the same, log the user in
#             if compare_images(image_data, get_previously_uploaded_image(username)):
#                 # Log the user in
#                 login(request, username)
#                 return redirect('home')
#             else:
#                 # The images are not the same, display an error message
#                 form.add_error(None, "The image does not match the previously uploaded image for this user.")
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def login_view(request):
#     # Check if the request method is POST
#     if request.method == 'POST':
#         face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#         cap = cv2.VideoCapture(0)
#         while True:
#             # Capture the video frame
#             ret, frame = cap.read()
#             # Convert the frame to grayscale
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#             # Detect faces in the frame
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#             if len(faces) > 0:
#                 # Get the coordinates of the detected face
#                 x, y, w, h = faces[0]
#                 # Crop the face from the frame
#                 face = frame[y:y+h, x:x+w]
#                 # Save the face to a file
#                 cv2.imwrite('face.jpg', face)
#                 break
#             # Release the video capture
#             cap.release()
#             # Destroy the window
#             cv2.destroyAllWindows()

#         captured_image = cv2.imread('face.jpg')
#         # Convert the image to a numpy array
#         image_array = np.fromstring(captured_image, np.uint8)

#         # Convert the numpy array to a cv2 image
#         image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

#         # Convert the image to grayscale
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         # Get the username from the request
#         username = request.POST['username']

#         # Get the user object for the given username
#         user = UserProfile.objects.get(username=username)

#         # Get the uploaded image for the given user
#         uploaded_image = user.image

#         # Convert the uploaded image to a numpy array
#         uploaded_image_array = np.fromstring(uploaded_image, np.uint8)

#         # Convert the uploaded image array to a cv2 image
#         uploaded_image = cv2.imdecode(uploaded_image_array, cv2.IMREAD_UNCHANGED)

#         # Convert the uploaded image to grayscale
#         uploaded_gray_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

#         # Compare the two images using cv2's matchTemplate function
#         res = cv2.matchTemplate(gray_image, uploaded_gray_image, cv2.TM_CCOEFF_NORMED)


#         # Check if the comparison result is above a certain threshold
#         if res > 0.8:
#             # If the images are a match, authenticate and login the user
#             user = authenticate(request, username=username)
#             login(request, user)
#             return redirect('home')
#         else:
#             # If the images are not a match, return an error message
#             return render(request, 'login.html', {'error': 'Invalid login'})
#     else:
#         form = LoginForm()
#         # If the request method is not POST, render the login page
#     return render(request, 'login.html', {'form':form})

def login_view(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Capture video from webcam
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
                face = frame[y:y+h, x:x+w]
                # Save the face to a file
                cv2.imwrite(r'capture1.jpg', face)
                break
        # Release the video capture
        cap.release()
        # Destroy the window
        cv2.destroyAllWindows()

        # Read the captured image
        captured_image = cv2.imread(r'capture1.jpg')
        # Convert the image to a numpy array
        image_array = np.fromstring(captured_image, np.uint8)
        # Convert the numpy array to a cv2 image
        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        # Convert the image to grayscale
        gray_image = image

        # Get the username from the request
        username = request.POST['username']

        from django.shortcuts import get_object_or_404

        # Get the user object for the given username or raise a 404 error if it does not exist
        user = get_object_or_404(UserProfile, username=username)
        if user is None:
        # If there is no user with the given username, return an error message
            return render(request, 'login.html', {'error': 'Invalid login'})

        # Get the uploaded image for the given user
        uploaded_image = user.image

        # Make sure that the uploaded_image object is a file-like object and is opened in binary mode
        if not isinstance(uploaded_image, (io.BufferedIOBase, io.TextIOBase)) or uploaded_image.mode != 'rb':
            raise ValueError('Invalid uploaded_image object')

        # Make sure  that the uploaded_image object is not closed
        if uploaded_image.closed:
            raise ValueError('uploaded_image object is closed')

        # Read the data from the uploaded_image object and store it in a numpy array
        uploaded_image_array = np.asarray(uploaded_image.read())

        # Decode the image data using the cv2.imdecode() function
        uploaded_image = cv2.imdecode(uploaded_image_array, cv2.IMREAD_UNCHANGED)

        # Convert the uploaded image to grayscale using the cv2.cvtColor() function
        uploaded_gray_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        # Set the comparison method and threshold
        method = cv2.TM_CCOEFF_NORMED
        threshold = 0.8

        # Compare the two images using cv2's matchTemplate function
        res = cv2.matchTemplate(gray_image, uploaded_gray_image, method)

        # Check if the comparison result is above the threshold
        if res > threshold:
            # If the images are a match, authenticate and login the user
            user = authenticate(request, username=username)
            login(request, user)
            return redirect('home')
        else:
            # If the images are not a match, return an error message
            return render(request, 'login.html', {'error': 'Invalid login'})
    else:
        form = LoginForm()
        # If the request method is not POST, render the login page
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
    return render(request, 'index.html', {})

# def Register(request):
#     return HttpResponse("login page bitch")

def SignIn(request):
    return HttpResponse("signin page bitch")







# Open a default webcam
        # cap = cv2.VideoCapture(0)

        # # Set the window name
        # cv2.namedWindow('webcam')

        # # Wait for 10 seconds
        # time.sleep(10)

        # # Read the frame from the webcam
        # ret, frame = cap.read()

        # # Save the frame to a file
        # cv2.imwrite('capture.jpg', frame)

        # # Read the captured image from the file
        # captured_image = cv2.imread('capture.jpg')

        # # Release the webcam and close all windows
        # cap.release()
        # cv2.destroyAllWindows()