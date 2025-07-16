// ฟังก์ชันสำหรับแสดง Pie Chart

function renderPieChart(canvasId, chartData) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const labels = Object.keys(chartData);
    const data = Object.values(chartData);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'จำนวนชั่วโมง',
                data: data,
                backgroundColor: generateColorSet(labels.length)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// ฟังก์ชันสุ่มสี (หรือจะใช้สีธีมก็ได้)
function generateColorSet(count) {
    const colors = [
        '#42a5f5', '#66bb6a', '#ffca28', '#ef5350',
        '#ab47bc', '#ffa726', '#26c6da', '#8d6e63'
    ];
    const selected = [];
    for (let i = 0; i < count; i++) {
        selected.push(colors[i % colors.length]);
    }
    return selected;
}
