import os
import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# API 키 설정
API_KEY = "YOUR_API_KEY"

# 헤더 설정
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# a 폴더에 새 이미지 파일이 추가되면 호출될 함수
def process_image(event):
    image_path = event.src_path
    image_url = f"file://{image_path}"

    # 작업 생성 요청
    data = {"image_url": image_url, "enable_pbr": True}
    response = requests.post("https://api.meshy.ai/v1/image-to-3d", json=data, headers=headers)
    task_id = response.json()["result"]

    # 작업 상태 확인
    while True:
        response = requests.get(f"https://api.meshy.ai/v1/image-to-3d/{task_id}", headers=headers)
        task_data = response.json()
        
        if task_data["status"] == "SUCCEEDED":
            fbx_url = task_data["model_urls"]["fbx"]
            break

    # FBX 파일 다운로드
    fbx_filename = os.path.join("b", os.path.basename(fbx_url))
    response = requests.get(fbx_url)

    with open(fbx_filename, "wb") as f:
        f.write(response.content)

    print(f"{fbx_filename} 파일이 다운로드되었습니다.")

# 이벤트 핸들러 생성
patterns = ["*"]
ignore_patterns = None
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
my_event_handler.on_created = process_image

# a 폴더 감시
path = "a"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)
my_observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    my_observer.stop()
my_observer.join()
