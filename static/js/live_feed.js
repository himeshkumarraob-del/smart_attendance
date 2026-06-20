(function () {
  const cfg = window.LIVE_FEED;
  if (!cfg) return;

  const video = document.getElementById('video');
  const canvas = document.createElement('canvas');
  const overlay = document.getElementById('overlay');
  const startBtn = document.getElementById('startBtn');
  const stopBtn = document.getElementById('stopBtn');
  const retrainBtn = document.getElementById('retrainBtn');
  const scanStatus = document.getElementById('scanStatus');
  const matchPanel = document.getElementById('matchPanel');
  const sessionLog = document.getElementById('sessionLog');

  let stream = null;
  let timer = null;

  function log(message) {
    const item = document.createElement('li');
    item.className = 'border-b border-slate-100 pb-2';
    item.textContent = `${new Date().toLocaleTimeString()} — ${message}`;
    sessionLog.prepend(item);
  }

  async function initCamera() {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
    video.srcObject = stream;
  }

  async function processFrame() {
    if (!video.videoWidth) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const image = canvas.toDataURL('image/jpeg', 0.85);

    const response = await fetch(cfg.processUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Recognition failed');

    overlay.innerHTML = '';
    data.results.forEach((result) => {
      const [top, right, bottom, left] = result.location;
      const box = document.createElement('div');
      box.className = 'match-box';
      box.style.top = `${(top / video.videoHeight) * 100}%`;
      box.style.left = `${(left / video.videoWidth) * 100}%`;
      box.style.width = `${((right - left) / video.videoWidth) * 100}%`;
      box.style.height = `${((bottom - top) / video.videoHeight) * 100}%`;
      overlay.appendChild(box);

      if (result.student) {
        const student = result.student;
        matchPanel.innerHTML = `
          <p class="font-semibold text-lg">${student.name}</p>
          <p class="text-slate-500">${student.roll} · ${student.student_code || ''}</p>
          <p class="mt-2">Confidence: <strong>${result.confidence}%</strong></p>
          <p class="mt-2 ${student.attendance_marked ? 'text-emerald-600' : 'text-slate-500'}">
            ${student.attendance_marked ? 'Attendance marked' : student.already_marked ? 'Already marked today' : 'Recognized'}
          </p>
        `;
        if (student.attendance_marked) {
          log(`Marked attendance for ${student.name} (${result.confidence}%)`);
        }
      } else if (result.unknown) {
        matchPanel.innerHTML = '<p class="text-amber-600">Unknown face detected.</p>';
      }
    });
  }

  startBtn.addEventListener('click', async () => {
    try {
      if (!stream) await initCamera();
      startBtn.disabled = true;
      stopBtn.disabled = false;
      scanStatus.textContent = 'Scanning...';
      timer = setInterval(() => {
        processFrame().catch((err) => {
          scanStatus.textContent = err.message;
        });
      }, 1500);
    } catch (err) {
      scanStatus.textContent = 'Camera error: ' + err.message;
    }
  });

  stopBtn.addEventListener('click', () => {
    clearInterval(timer);
    timer = null;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    scanStatus.textContent = 'Scanning stopped.';
  });

  retrainBtn.addEventListener('click', async () => {
    retrainBtn.disabled = true;
    scanStatus.textContent = 'Retraining model...';
    try {
      const response = await fetch(cfg.retrainUrl, { method: 'POST' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Retrain failed');
      scanStatus.textContent = `Model retrained with ${data.count} encodings.`;
      log(`Retrained model (${data.count} encodings).`);
    } catch (err) {
      scanStatus.textContent = err.message;
    } finally {
      retrainBtn.disabled = false;
    }
  });
})();
