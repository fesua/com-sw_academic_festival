from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST']) # GET, POST 메서드 허용
def upload_file():
    if request.method == 'POST': # POST 요청일 때만 파일 업로드 처리
        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        print(f'File {file.filename} uploaded successfully')
        return 'File uploaded successfully'
    
    # GET 요청일 경우 파일 업로드 폼 렌더링
    return '''
        <!doctype html>
        <title>Upload File</title>
        <h1>Upload File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
