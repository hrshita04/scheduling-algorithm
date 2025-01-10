let processes = [];
let pid = 1;

document.getElementById('add-process').addEventListener('click', () => {
    const arrivalTime = parseInt(document.getElementById('arrival-time').value);
    const burstTime = parseInt(document.getElementById('burst-time').value);

    if (isNaN(arrivalTime) || isNaN(burstTime)) {
        alert("Please enter valid arrival and burst times.");
        return;
    }

    processes.push({ pid: pid++, arrival_time: arrivalTime, burst_time: burstTime });

    const tableBody = document.querySelector('#process-table tbody');
    const row = document.createElement('tr');
    row.innerHTML = `<td>${pid - 1}</td><td>${arrivalTime}</td><td>${burstTime}</td>`;
    tableBody.appendChild(row);

    document.getElementById('arrival-time').value = '';
    document.getElementById('burst-time').value = '';
});

document.getElementById('algorithm').addEventListener('change', (e) => {
    const timeQuantumInput = document.getElementById('time-quantum');
    const timeQuantumLabel = document.getElementById('time-quantum-label');
    if (e.target.value === 'RR') {
        timeQuantumInput.style.display = 'inline';
        timeQuantumLabel.style.display = 'inline';
    } else {
        timeQuantumInput.style.display = 'none';
        timeQuantumLabel.style.display = 'none';
    }
});

document.getElementById('visualize').addEventListener('click', () => {
    const algorithm = document.getElementById('algorithm').value;
    const timeQuantum = parseInt(document.getElementById('time-quantum').value);

    const payload = {
        algorithm: algorithm,
        processes: processes,
        time_quantum: algorithm === 'RR' ? timeQuantum : null
    };

    fetch('/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                renderGanttChart(data);
            }
        });
});

function renderGanttChart(ganttChart) {
    const chartDiv = document.getElementById('gantt-chart');
    chartDiv.innerHTML = '';

    ganttChart.forEach(block => {
        const blockDiv = document.createElement('div');
        blockDiv.style.display = 'inline-block';
        blockDiv.style.width = `${block.end - block.start}em`;
        blockDiv.style.backgroundColor = block.pid === 'Idle' ? '#ddd' : '#007BFF';
        blockDiv.style.color = 'white';
        blockDiv.style.textAlign = 'center';
        blockDiv.style.padding = '5px';
        blockDiv.textContent = block.pid;
        chartDiv.appendChild(blockDiv);
    });
}
