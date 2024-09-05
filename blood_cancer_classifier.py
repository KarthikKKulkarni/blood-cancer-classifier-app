import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import tensorflow as tf
import numpy as np
import os

# Ensure the working directory is the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load the Keras .h5 model
try:
    model = tf.keras.models.load_model("bloodcell.h5")
except Exception as e:
    print(f"Error loading model: {e}")

# Define the class labels
class_labels = ['Benign', 'Malignant_Pre-B', 'Malignant_Pro-B', 'Malignant_early Pre-B']

# Function to preprocess and classify an image
def classify_image():
    file_path = file_path_label.cget("text")
    if file_path:
        try:
            # Load and preprocess the image
            img = Image.open(file_path).resize((224, 224))  # Resize to the input size your model expects
            img_array = np.array(img, dtype=np.float32)
            img_array = img_array / 255.0  # Normalize pixel values to [0, 1]
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

            # Perform prediction
            predictions = model.predict(img_array)

            # Get the predicted class and probability
            predicted_class_index = np.argmax(predictions)
            predicted_class_label = class_labels[predicted_class_index]
            probability = predictions[0][predicted_class_index] * 100

            # Update and display the result with frame styling
            result_frame.pack()
            result_label.config(
                text=f"Predicted Class: {predicted_class_label}\nProbability: {probability:.2f}%",
                bg="#f0f8ff",  # Light background color for the result frame
                font=("Arial", 12, "bold")
            )
            result_frame.config(
                bg="#d3d3d3",  # Light gray background for the frame
                borderwidth=2,
                relief="sunken"
            )
        except Exception as e:
            print(f"Error during classification: {e}")

# Function to handle file upload and display image preview
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        try:
            # Update the file path label with the selected file path
            file_path_label.config(text=file_path)

            # Display the uploaded image preview
            img = Image.open(file_path)
            img = img.resize((200, 200), Image.LANCZOS)  # Resize for preview
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk  # Keep a reference to prevent garbage collection
            print(f"Image preview updated: {file_path}")
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(image='')  # Clear the image label if there is an error

# Create a Tkinter window
window = tk.Tk()
window.title("Blood Cancer Classifier")

# Create a button to upload an image
upload_button = tk.Button(window, text="Upload Image", command=upload_file)
upload_button.pack(pady=20)

# Create a label to display the file path of the uploaded image
file_path_label = tk.Label(window, wraplength=300)
file_path_label.pack()

# Create a frame to display the uploaded image
image_frame = tk.Frame(window)
image_frame.pack()

# Create a label to display the uploaded image
image_label = tk.Label(image_frame)
image_label.pack()

# Create a "Classify" button
classify_button = tk.Button(window, text="Classify", command=classify_image)
classify_button.pack(pady=10)

# Create a frame for the result page (hidden initially)
result_frame = tk.Frame(window, bg="#d3d3d3", borderwidth=2, relief="sunken")
result_label = tk.Label(result_frame, bg="#f0f8ff", font=("Arial", 12, "bold"))
result_label.pack(pady=10, padx=10)

# Create a button to close the result page
close_button = tk.Button(result_frame, text="Close", command=result_frame.pack_forget)
close_button.pack(pady=10)

# Create an "Exit" button
exit_button = tk.Button(window, text="Exit", command=window.quit)
exit_button.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
