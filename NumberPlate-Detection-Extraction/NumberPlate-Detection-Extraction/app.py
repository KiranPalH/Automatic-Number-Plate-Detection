from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from deeplearning import object_detection
import time
import threading

app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static/upload/')

start_time = None
timer_thread = None
timer_lock = threading.Lock()
base_price = 5.0
price_per_second = 0.01


def start_timer():
    global start_time
    with timer_lock:
        if start_time is None:
            start_time = time.time()
            print(f"Timer started at: {start_time}")
    while True:
        with timer_lock:
            if start_time is None:
                break
        time.sleep(1)


def stop_timer():
    global start_time
    with timer_lock:
        if start_time is not None:
            elapsed_time = time.time() - start_time
            print(f"Timer stopped at: {time.time()} after {elapsed_time} seconds")
            start_time = None
            total_cost = base_price + elapsed_time * price_per_second
            print(f"Total cost calculated: {total_cost}")
            return elapsed_time, total_cost
    print("Timer was not running")
    return 0, base_price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        text_list = object_detection(path_save, filename)
        
        global timer_thread
        if timer_thread is None or not timer_thread.is_alive():
            timer_thread = threading.Thread(target=start_timer)
            timer_thread.start()
        
        return render_template('index.html', upload=True, upload_image=filename, text=text_list, no=len(text_list))

    return render_template('index.html', upload=False)


@app.route('/stop_timer', methods=['POST'])
def stop_timer_route():
    elapsed_time, total_cost = stop_timer()
    return jsonify({'elapsed_time': elapsed_time, 'total_cost': total_cost})


@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_text = request.form['feedback']
    with open('feedback.txt', 'a') as f:
        f.write(f"{feedback_text}\n")
    return redirect(url_for('index', feedback_submitted=True))


if __name__ == "__main__":
    app.run(debug=True)
