# AI--Object-Detection
Used YOLOV8 for AI real time Object Detection. Self trained with images 1200+ taken. Used Python to make actions on the screen for it to interact with a game.
Code needs trained model which is provided, need to change directory as it is set to my files
name of window will need to be changed as it is set to my account
made only for learning purposes - do not use for anything else 
may need more files, free feel to email me if it does not work - Arsh.singh.sandhu1@gmail.com
roboflow dataset- https://universe.roboflow.com/arshdeep-sandhu-huxgg/attacks2
i cannot put trained model here so if you would like to train yourself feel free:
steps:
download roboflow zip and unzip
change settings.yaml for directory to the data.yaml of attacks2new
make sure all of YOLOv8 steps are downloaded
make sure cpu is able to be used, if using nvidia will need to download toolkit
run in terminal: yolo task=detect mode=train model=yolov8s.pt data=attacksnew2/data.yaml epochs=400 imgsz=992,653 device=0 batch=10
if it does not work, turn down batch size
