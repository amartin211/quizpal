from ultralytics import YOLO

# Load a model
model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(
    data="/home/aime/python-environments/exam_script_deploy/dataset/dataset.yaml",
    epochs=100,
    imgsz=640,
    device=[0, 1],
)
