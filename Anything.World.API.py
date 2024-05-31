import os
import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# fbx 저장 위치
save_folder = ""

# API 키 설정
API_KEY = ''

# API 엔드포인트 설정
BASE_URL = 'https://api.anything.world/v2/'

# 요청 헤더 설정
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# 리깅 요청 함수
def rig_model():
    model_id = "dog" # dog or cat만 동작하는데 같은 방식으로 처리
    url = f'{BASE_URL}rigging'
    payload = {
        'model_id': model_id
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        download_and_save_object(response.json().get('id'), save_folder)
        return
    else:
        return f"Error: {response.status_code}, {response.text}"

# 리깅 상태 확인 함수
def check_rigging_status(rigging_id):
    url = f'{BASE_URL}rigging/{rigging_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# 리깅된 오브젝트 다운로드 및 저장 함수
def download_and_save_object(rigging_id, save_folder):
    global save_folder
    status_response = check_rigging_status(rigging_id)
    if status_response.get('status') == 'completed':
        object_url = status_response.get('object_url')  # 오브젝트 URL 추출
        response = requests.get(object_url)
        if response.status_code == 200:
            file_name = os.path.join(save_folder, f'{rigging_id}.zip')
            with open(file_name, 'wb') as file:
                file.write(response.content)
            return f"File saved to {file_name}"
        else:
            return f"Error downloading file: {response.status_code}, {response.text}"
    else:
        return "Rigging not completed yet."

# 이벤트 핸들러 생성
patterns = ["*"]
ignore_patterns = None
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
my_event_handler.on_created = rig_model

# 폴더 감시
path = "" # 감시할 폴더
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
