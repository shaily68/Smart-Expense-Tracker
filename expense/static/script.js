// Wait for DOM to load
document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("expenseChart");

  // Check if the chart element exists
  if (!ctx) {
    console.warn("Chart canvas not found.");
    return;
  }

  // Initialize pie chart
  const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Food', 'Transport', 'Groceries', 'Bills'], // Example categories
      datasets: [{
        label: 'Expenses',
        data: [200, 150, 100, 50], // Example data (you can make dynamic later)
        backgroundColor: [
          '#f39c12', // orange
          '#3498db', // blue
          '#2ecc71', // green
          '#e74c3c'  // red
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#333',
            font: {
              size: 14
            }
          }
        }
      }
    }
  });
});
