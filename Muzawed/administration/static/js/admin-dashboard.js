document.addEventListener('DOMContentLoaded', function () {
  const chartElement = document.getElementById('userChart');

  if (chartElement) {
    const suppliersCount     = Number(chartElement.dataset.suppliers);
    const beneficiariesCount = Number(chartElement.dataset.beneficiaries);
    const totalUsers         = Number(chartElement.dataset.total);

    const ctx = chartElement.getContext('2d');

    const userChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['الموردين', 'المستفيدين', 'إجمالي المستخدمين'],
        datasets: [{
          label: 'عدد المستخدمين',
          data: [suppliersCount, beneficiariesCount, totalUsers],
          backgroundColor: ['#204a3a', '#e67e22', '#4A3A20'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { font: { size: 12 } }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.label + ': ' + context.parsed;
              }
            }
          }
        }
      }
    });
  }


  
});
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('show');
}
