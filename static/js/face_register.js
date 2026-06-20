(function () {
  const cfg = window.FACE_REGISTER;
  if (!cfg) return;

  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const captureBtn = document.getElementById('captureBtn');
  const finalizeBtn = document.getElementById('finalizeBtn');
  const statusEl = document.getElementById('status');
  const gallery = document.getElementById('gallery');
  const progressBar = document.getElementById('progressBar');
  const progressLabel = document.getElementById('progressLabel');

  let stream = null;
  let captured = cfg.captured || 0;
  let captureIndex = captured;

  function updateProgress() {
    const pct = Math.min(100, (captured / cfg.target) * 100);
    progressBar.style.width = `${pct}%`;
    progressLabel.textContent = `${captured} / ${cfg.target}`;
    finalizeBtn.disabled = captured < 1;
  }

  async function initCamera() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
      video.srcObject = stream;
      statusEl.textContent = 'Camera ready. Capture multiple angles for best accuracy.';
    } catch (err) {
      statusEl.textContent = 'Unable to access camera: ' + err.message;
      captureBtn.disabled = true;
    }
  }

  captureBtn.addEventListener('click', async () => {
    if (!stream) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const image = canvas.toDataURL('image/jpeg', 0.92);

    captureBtn.disabled = true;
    statusEl.textContent = 'Uploading capture...';

    try {
      const response = await fetch(cfg.uploadUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image, index: captureIndex }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      captured = data.count;
      captureIndex += 1;
      updateProgress();

      const item = document.createElement('div');
      item.className = 'aspect-square rounded-lg overflow-hidden border border-slate-200';
      item.innerHTML = `<img src="${image}" alt="Captured face">`;
      gallery.prepend(item);

      statusEl.textContent = 'Capture saved successfully.';
    } catch (err) {
      statusEl.textContent = err.message;
    } finally {
      captureBtn.disabled = false;
    }
  });

  finalizeBtn.addEventListener('click', async () => {
    finalizeBtn.disabled = true;
    statusEl.textContent = 'Training face model...';

    try {
      const response = await fetch(cfg.completeUrl, { method: 'POST' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Finalize failed');
      statusEl.textContent = `Registration complete. ${data.encodings} encodings loaded.`;
    } catch (err) {
      statusEl.textContent = err.message;
      finalizeBtn.disabled = false;
    }
  });

  updateProgress();
  initCamera();
})();
