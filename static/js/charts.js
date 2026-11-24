document.addEventListener("DOMContentLoaded", function () {
  const rawData = document.getElementById("chart-data");
  if (!rawData) return;
  const chartData = JSON.parse(rawData.textContent);

  new Chart(document.getElementById("debtChart"), {
    type: "line",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: "Sisa Hutang (Cicilan Standar)",
          data: chartData.saldo_standar,
          borderColor: "#0d6efd",
          backgroundColor: "rgba(13, 110, 253, 0.1)",
          fill: true,
          tension: 0.3,
        },
        {
          label: "Sisa Hutang (Saran Akselerasi ML)",
          data: chartData.saldo_akselerasi,
          borderColor: "#198754",
          borderDash: [5, 5],
          fill: false,
          tension: 0.3,
        },
      ],
    },
  });

  new Chart(document.getElementById("budgetChart"), {
    type: "doughnut",
    data: {
      labels: ["Cicilan Hutang", "Kebutuhan Pokok", "Tabungan & Sisa Kas"],
      datasets: [
        {
          data: chartData.alokasi,
          backgroundColor: ["#dc3545", "#ffc107", "#198754"],
        },
      ],
    },
  });
});
