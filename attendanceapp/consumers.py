import json
from channels.generic.websocket import WebsocketConsumer

# The camera consumer takes image data from the webcam (sent over websockets)
# and sends back the processed metadata.

# Eventually, this is where code teams 1 and 2 will work their magic. But for
# now, it just returns a dumb placeholder value: the length of the string
# representing the encoded image.


class CameraConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data[0:100])
        self.send(text_data=json.dumps({
            'length': len(text_data)
        }))
