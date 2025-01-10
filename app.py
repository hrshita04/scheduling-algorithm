from flask import Flask, render_template, request, jsonify
from scheduler import fcfs, sjf, round_robin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    algorithm = data.get('algorithm')
    processes = data.get('processes')
    time_quantum = data.get('time_quantum', None)

    if algorithm == 'FCFS':
        gantt_chart = fcfs(processes)
    elif algorithm == 'SJF':
        gantt_chart = sjf(processes)
    elif algorithm == 'RR' and time_quantum:
        gantt_chart = round_robin(processes, time_quantum)
    else:
        return jsonify({"error": "Invalid input"}), 400

    return jsonify(gantt_chart)

if __name__ == '__main__':
    app.run(debug=True)
