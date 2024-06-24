from ultralytics import YOLO

# Load a model
model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="vision/yolo_custom.yaml", epochs=100, imgsz=640, device=[0, 1])
