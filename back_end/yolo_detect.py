import json
import cv2
import datetime
from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path="yolo11n.pt", confidence_threshold=0.5, collection_name="object"):
        
        #YOLO 객체 탐지
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.collection_name = collection_name


    def detect_objects(self, image_path):
        
        #이미지에서 객체를 탐지 후 MongoDB에 저장
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ 오류: '{image_path}' 이미지를 찾을 수 없음")
            return json.dumps({"error": "Image not found"}, indent=4)

        # 객체 탐지 수행
        results = self.model(image)

        detected_objects = []
        for result in results:
            for box in result.boxes:
                if box.conf >= self.confidence_threshold:
                    class_id = int(box.cls)
                    class_name = self.model.names[class_id]
                    bbox = [round(x.item(), 2) for x in box.xyxy[0]]

                    object_data = {
                        "name": class_name,
                        "bounding_box": {
                            "x1": bbox[0],
                            "y1": bbox[1],
                            "x2": bbox[2],
                            "y2": bbox[3]
                        },
                        "create_date": datetime.datetime.now().isoformat()
                    }
                    detected_objects.append(object_data)

        
        # JSON 형식으로 반환 (ObjectId -> str 변환)
        return json.dumps(detected_objects, indent=4)


# 실행 예제
if __name__ == "__main__":
    detector = YOLODetector()
    image_path = "test.jpg"  # 사용하고 싶은 이미지 경로 설정
    result_json = detector.detect_objects(image_path)
    print(result_json)
    
  