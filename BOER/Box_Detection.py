import os
import cv2
from ultralytics import YOLO

global confidence_threshold

# Modeli yükle
def initialize_model():
    global model
    model = YOLO(model_path)
    global labels
    labels = model.names

def set_confidence_threshold(threshold):
    global confidence_threshold
    confidence_threshold = threshold

def set_model_path(path):
    global model_path
    model_path = path
    initialize_model()

def Detect_Boxes(frame):
    result = model(frame, verbose=False)[0]
    
    box_coordinates = []
    box_names = []
    box_confidence = []

    for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
        if conf.item() < confidence_threshold:
            continue

        coords = box.cpu().numpy().squeeze().astype(int)
        class_name = labels[int(cls.item())]

        box_coordinates.append(coords)
        box_names.append(class_name)
        box_confidence.append(round(conf.item() * 100, 2))  # Yüzde ve yuvarlama

    print("Boxes detected")
    return box_coordinates, box_names, box_confidence

def Draw_Boxes(frame, box_coordinates, box_names, box_confidence):
    bbox_colors = [(164, 120, 87), (68, 148, 228), (93, 97, 209), (178, 182, 133)]

    for i, (coords, name, conf) in enumerate(zip(box_coordinates, box_names, box_confidence)):
        color = bbox_colors[i % len(bbox_colors)]
        x1, y1, x2, y2 = coords

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f'{name}: {conf}%'
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    print("Boxes drawn")
    return frame
# Makes a .txt file
def Export_Box_Coordinates(box_coordinates, box_names, box_confidence, output_file):
    output_file = output_file.replace(".jpg", ".txt")
    with open(output_file, 'w') as f:
        for coords, name, conf in zip(box_coordinates, box_names, box_confidence):
            f.write(f"{name};{conf};{coords[0]},{coords[1]};{coords[2]},{coords[3]}\n")
    return output_file

def Open_Image(image_path):
    if not os.path.exists(image_path):
        print(f"Can not find image: {image_path}")
        return None
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None
    print('Image opened.')
    return image

def Save_Image(frame, output_path):
    cv2.imwrite(output_path, frame)
    print(f"Image saved")