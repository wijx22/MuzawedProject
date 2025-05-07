document.addEventListener('DOMContentLoaded', function () {
  const chartElement = document.getElementById('userChart');

  if (chartElement) {
    const suppliersCount     = Number(chartElement.dataset.suppliers);
    const beneficiariesCount = Number(chartElement.dataset.beneficiaries);
    const totalUsers        = Number(chartElement.dataset.total);

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

  // رسم حالات الموردين
  const statusChartElement = document.getElementById('supplyStatusChart');

  if (statusChartElement) {
    const acceptedCount = Number(statusChartElement.dataset.accepted);
    const rejectedCount = Number(statusChartElement.dataset.rejected);
    const pendingCount  = Number(statusChartElement.dataset.pending);
    const noRequestCount = Number(statusChartElement.dataset.noRequest);  // إضافة الحالة "لا طلب"

    const ctxStatus = statusChartElement.getContext('2d');

    const supplyStatusChart = new Chart(ctxStatus, {
      type: 'doughnut',
      data: {
        labels: ['مقبول', 'مرفوض', 'قيد المعالجة', 'لا طلب'],  // إضافة "لا طلب"
        datasets: [{
          label: 'حالات الموردين',
          data: [acceptedCount, rejectedCount, pendingCount, noRequestCount],  // إضافة "لا طلب"
          backgroundColor: ['#4CAF50', '#F44336', '#FFC107', '#B0BEC5'],  // إضافة لون للـ "لا طلب"
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
                return context.label + ': ' + context.parsed + ' مورد';
              }
            }
          }
        }
      }
    });
  }


    // رسم الرسم البياني العمودي المكدس لحالات الطلبات
    const barChartElement = document.getElementById('myChart');

    if (barChartElement) {
      const ctxBar = barChartElement.getContext('2d');
  
      const xValues = ["طلب 1", "طلب 2", "طلب 3", "طلب 4", "طلب 5"];
      const processed = [20, 30, 10, 25, 15]; 
      const pending = [10, 5, 15, 5, 10];     
      const accepted = [25, 14, 19, 8, 5];    
  
      new Chart(ctxBar, {
        type: "bar",
        data: {
          labels: xValues,
          datasets: [
            {
              label: "معالجة",
              backgroundColor: "blue",
              data: processed
            },
            {
              label: "مقيدة",
              backgroundColor: "orange",
              data: pending
            },
            {
              label: "مقبولة",
              backgroundColor: "green",
              data: accepted
            }
          ]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: "حالة طلبات التوريد"
            }
          },
          scales: {
            x: {
              stacked: true
            },
            y: {
              stacked: true,
              beginAtZero: true
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

