from mss import mss
import torch, torchvision
print(torch.__version__, torch.cuda.is_available())
import torchvision.transforms as T
import torch.nn.functional as F
from torchvision.transforms import functional as F
torch.set_grad_enabled(False)
#%matplotlib inline
import numpy as np
import mss
import cv2
from torchvision.transforms import Compose, ToTensor, Resize
from PIL import Image
from win32api import GetSystemMetrics

#Loading in model
num_classes = 2

transform = T.Compose([
    T.Resize((640)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

model = torch.hub.load('facebookresearch/detr',
                       'detr_resnet50',
                       pretrained=False,
                       num_classes=num_classes)

checkpoint = torch.load('outputs/checkpoint.pth',
                        map_location='cpu')

model.load_state_dict(checkpoint['model'],
                      strict=False)

model.eval();


def grab_screen(width, height):

    with mss.mss() as sct:    
        
        # Set to 180 to trim top, could be adjusted accordingly
        region=(0, 180, int(width/2), int(height))
        region = {'left': region[0], 'top': region[1], 'width': region[2] - region[0], 'height': region[3] - region[1]}
        
        sct_img = sct.grab(region)

        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return img

# Preprocessing image 
def preprocess_image(img):
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert the numpy array to a PIL Image
    img_pil = F.to_pil_image(img_rgb)

    img_tensor = transform(img_pil)

    return img_tensor.unsqueeze(0)  

def main():
    
    if torch.cuda.is_available():
        model.cuda()

    #Creates the window 
    cv2.namedWindow('Detected Poles', cv2.WINDOW_NORMAL)
    
    while True:
        
        # Gets resolution width and height from system
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)

        screen = grab_screen(width, height)

        # Scales window resolution
        img = cv2.resize(screen, None, fx=1, fy=1)

        # Preprocess the image for DETR
        img_tensor = preprocess_image(img)

        if torch.cuda.is_available():
            img_tensor = img_tensor.cuda()
            

        # Inference/ Passes it through the model
        with torch.no_grad():
            outputs = model(img_tensor)

        # Keeps those above confidence level threshold
        threshold = 0.9
        probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
        keep = probas.max(-1).values > threshold

        #Converts bounding box coordinates
        bboxes_scaled = bb_coord(outputs['pred_boxes'][0, keep].cpu(), img.shape[:2])

        #Draws bounding boxes
        for bbox, proba in zip(bboxes_scaled, probas[keep]):

            x_min, y_min, x_max, y_max = bbox

            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(img, str(round(proba.tolist()[1], 6)), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)


        #Put number of poles detected
        cv2.putText(img, str(len(bboxes_scaled)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        

        ## Formatting display window
    
        # Resizes window to half of screen by default
        cv2.resizeWindow("Detected Poles", int(width/2), int(height))

        # Displays window
        cv2.imshow('Detected Poles', img)

        #Moves window to right half of monitor 
        cv2.moveWindow("Detected Poles", int(width/2), 0) 
        
        ##

        #Press 'q' to end program
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Converts bounding box coordinates to pixel
def bb_coord(out_bbox, size):
    img_h, img_w = size[0], size[1]
    bboxes_scaled = []
    for bbox in out_bbox:
        cx, cy, w, h = bbox
        x_min = int((cx - w / 2) * img_w)
        y_min = int((cy - h / 2) * img_h)
        x_max = int((cx + w / 2) * img_w)
        y_max = int((cy + h / 2) * img_h)
        bboxes_scaled.append([x_min, y_min, x_max, y_max])
    return bboxes_scaled

if __name__ == "__main__":
    main()


