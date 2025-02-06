from ultralytics import YOLO
import cv2
import json

# YOLOv11 'nano' 모델 로드
model = YOLO('yolo11n.pt')  # 처음 실행 시 자동으로 다운로드됩니다.

# 이미지 로드
image_path = 'sample.jpg'  # 처리할 이미지의 경로를 지정하세요
image = cv2.imread(image_path)

# 객체 탐지 수행
results = model(image)

# 임계값 설정
confidence_threshold = 0.5  # 원하는 정확도 임계값을 설정하세요

# 탐지된 객체 정보를 저장할 리스트
detected_objects = []

# 탐지된 객체 정보 추출 및 출력
for result in results:
    for box in result.boxes:
        if box.conf >= confidence_threshold:
            class_id = int(box.cls)
            class_name = model.names[class_id]
            bbox = [round(x.item(), 2) for x in box.xyxy[0]]  # 바운딩 박스 좌표 (x1, y1, x2, y2)

            object_data = {
                "object_name": class_name,
                "confidence": round(box.conf.item(), 2),
                "bounding_box": {
                    "x1": bbox[0],
                    "y1": bbox[1],
                    "x2": bbox[2],
                    "y2": bbox[3]
                }
            }
            detected_objects.append(object_data)

# JSON 형식으로 변환 (MongoDB 저장 가능)
json_output = json.dumps(detected_objects, indent=4)
print(json_output)
