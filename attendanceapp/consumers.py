import json
from channels.generic.websocket import WebsocketConsumer
import face_recognition
from attendanceapp.models import Photo
from io import BytesIO
from binascii import a2b_base64

# The camera consumer takes image data from the webcam (sent over websockets)
# and sends back the processed metadata.

# Eventually, this is where code teams 1 and 2 will work their magic. But for
# now, it just returns a dumb placeholder value: the length of the string
# representing the encoded image.


class CameraConsumer(WebsocketConsumer):
    face_encodings = []

    def connect(self):
        self.accept()

        # Get all photos stored in database (which were uploaded using the admin page)
        photo_objects = Photo.objects.order_by("person__name").all()

        self.face_encodings = get_face_encodings_from_photo_objects(
            photo_objects)

    def disconnect(self, close_code):
        print("Disconnecting")
        pass

    def receive(self, text_data):
        # The variable text_data contains a frame from the webcam
        # encoded as a string that looks something like
        # "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAA..."
        # Here we treat that image data like a file and get its
        # face_recognition encodings
        binary_data = a2b_base64(text_data.split(",")[1])
        if (len(binary_data) > 0):
            binary_file = BytesIO(binary_data)
            webcam_photo = face_recognition.load_image_file(binary_file)
            webcam_photo_encodings = face_recognition.face_encodings(
                webcam_photo)
        else:
            webcam_photo_encodings = []

        # Now, for each face (encoding) in the webcam photo, compare it
        # to all the faces (encodings) we have saved in the database
        # And store all the results in webcam_faces
        webcam_faces = []
        for webcam_photo_encoding in webcam_photo_encodings:
            percentages = list(face_recognition.face_distance(
                [data["encoding"] for data in self.face_encodings], webcam_photo_encoding))

            matches = []
            for index, percentage in enumerate(percentages):
                matches.append({
                    "person": self.face_encodings[index]["person"]["name"],
                    "percentage": 1 - percentage  # `percentage` is the "distance", but we want similarity
                })

            webcam_faces.append({
                "matches": matches
            })

        # Finally, send the webcam_faces data back to the client
        self.send(text_data=json.dumps({
            "faces": webcam_faces
        }))


def get_face_encodings_from_photo_objects(photo_objects):
    face_encodings = []

    for photo_object in photo_objects:
        print(photo_object.person.name,
              photo_object.person.id, photo_object.image.path)

        # Load image file as numpy array
        photo = face_recognition.load_image_file(photo_object.image.path)

        # Get list of vector encodings for all faces in image
        encodings = face_recognition.face_encodings(photo)

        if (len(encodings) == 0):
            print("Photo {file_name} of {person_name} does not appear to contain any faces".format(
                file_name=photo_object.image.name, person_name=photo_object.person.name))
        else:
            encoding = encodings[0]
            face_encodings.append({
                "person": {
                    "id": photo_object.person.id,
                    "name": photo_object.person.name,
                },
                "encoding": encoding
            })

    return face_encodings
