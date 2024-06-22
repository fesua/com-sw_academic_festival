import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def run_code(event):
    file_path = event.src_path
    if file_path.endswith('.jpg') or file_path.endswith('.png'):
        cmd = f"python tools/predict.py --config configs/ppmattingv2/ppmattingv2-stdc1-human_512.yml --model_path pretrained_models/ppmattingv2-stdc1-human_512.pdparams --image_path {file_path} --save_dir ./output/results --fg_estimate True"
        subprocess.run(cmd, shell=True)

patterns = ["*"]
ignore_patterns = None
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
my_event_handler.on_created = run_code

path = "." # 감시할 폴더 경로를 여기에 설정하세요.

go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)
my_observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
my_observer.join()
