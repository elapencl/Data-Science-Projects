import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
import urllib.request

image_url = 'https://media.gettyimages.com/photos/republican-presidential-nominee-donald-trump-pauses-during-a-campaign-picture-id599724318?s=2048x2048'
face_api_url = 'https://elapencl.cognitiveservices.azure.com/face/v1.0/detect'
params = {
    'detectionModel': 'detection_01',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    'returnFaceId': 'true'
}

image_data = urllib.request.urlopen(image_url).read()
headers = {'Ocp-Apim-Subscription-Key': 'e29c7de50749413c92b8ba05c1a9929d'}
response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
responseJson = response.json()
print(responseJson)
genderId = responseJson[0]['faceAttributes']['gender']
ageId = str(int(responseJson[0]['faceAttributes']['age']))
emotionId = responseJson[0]['faceAttributes']['emotion']
maxemotion_value = 0
for item in emotionId:
    if emotionId[item] > maxemotion_value:
        maxemotion_value = emotionId[item]
        identified_emotion = item

bbox = []
face_rectangle = responseJson[0]['faceRectangle']
for item in face_rectangle:
    bbox.append(face_rectangle[item])

image = Image.open(BytesIO(image_data))
plt.imshow(image).axes.add_patch(Rectangle((bbox[1], bbox[0]), bbox[2], bbox[3], fill=False, linewidth=2, color='r'))
plt.annotate(genderId + ", " + ageId, (bbox[1], bbox[0]), textcoords='offset points', xytext=(0,0), ha='left',va='bottom',color='white',weight='bold',backgroundcolor='black')
plt.annotate('facial expression: ' + identified_emotion, (bbox[1], bbox[0]+bbox[3]), textcoords = 'offset points', xytext=(0, 0), ha='left', va='top', color='white', weight='bold', backgroundcolor = 'black')
plt.axis('off')
plt.show()
