/* =====================================
   DONATION ANALYTICS CHART
===================================== */
document.addEventListener("DOMContentLoaded", () => {

    const canvas = document.getElementById("monthlyChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    const gradient = ctx.createLinearGradient(0, 0, 0, 350);

    gradient.addColorStop(0, "rgba(37,99,235,0.35)");
    gradient.addColorStop(1, "rgba(37,99,235,0)");

    new Chart(ctx, {

        type: "line",

        data: {

            labels: monthlyLabels,

            datasets: [{

                label: "Monthly Donations",

                data: monthlyTotals,

                borderColor: "#2563eb",

                backgroundColor: gradient,

                fill: true,

                borderWidth: 4,

                tension: 0.45,

                pointRadius: 5,

                pointHoverRadius: 8,

                pointBackgroundColor: "#ffffff",

                pointBorderColor: "#2563eb",

                pointBorderWidth: 3

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {

                intersect: false,

                mode: "index"

            },

            plugins: {

                legend: {

                    display: false

                },

                tooltip: {

                    backgroundColor: "#111827",

                    titleColor: "#fff",

                    bodyColor: "#fff",

                    padding: 14,

                    cornerRadius: 12,

                    displayColors: false,

                    callbacks: {

                        label: function(context){

                            return " KSh " + context.raw.toLocaleString();

                        }

                    }

                }

            },

            scales: {

                x: {

                    grid: {

                        display: false

                    },

                    ticks: {

                        color: "#64748b",

                        font: {

                            weight: "600"

                        }

                    }

                },

                y: {

                    beginAtZero: true,

                    grid: {

                        color: "#eef2f7"

                    },

                    ticks: {

                        color: "#64748b",

                        callback: function(value){

                            return "KSh " + value.toLocaleString();

                        }

                    }

                }

            },

            animation: {

                duration: 1800,

                easing: "easeOutQuart"

            }

        }

    });

});