(function () {
  const cfg = window.ANALYTICS;
  if (!cfg) return;

  fetch(cfg.dataUrl)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('summaryStudents').textContent = data.summary.total_students;
      document.getElementById('summaryPresent').textContent = data.summary.present_today;
      document.getElementById('summaryRate').textContent = `${data.summary.attendance_rate}%`;

      const trendLabels = data.trends.map((row) => row.date.slice(5));
      const trendCounts = data.trends.map((row) => row.count);

      new Chart(document.getElementById('trendChart'), {
        type: 'line',
        data: {
          labels: trendLabels,
          datasets: [{
            label: 'Daily Attendance',
            data: trendCounts,
            borderColor: '#2563eb',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: true,
            tension: 0.35,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
        },
      });

      new Chart(document.getElementById('deptChart'), {
        type: 'bar',
        data: {
          labels: data.departments.map((row) => row.name),
          datasets: [{
            label: 'Attendance Count',
            data: data.departments.map((row) => row.count),
            backgroundColor: '#0f172a',
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
        },
      });

      const body = document.getElementById('rankingsBody');
      data.rankings.forEach((row, index) => {
        const tr = document.createElement('tr');
        tr.className = 'border-b border-slate-100';
        tr.innerHTML = `
          <td class="py-2 pr-4">${index + 1}</td>
          <td class="py-2 pr-4">${row.name}</td>
          <td class="py-2">${row.count}</td>
        `;
        body.appendChild(tr);
      });
    })
    .catch((err) => {
      console.error(err);
    });
})();
