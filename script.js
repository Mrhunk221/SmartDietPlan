document.addEventListener("DOMContentLoaded", () => {
    const dietForm = document.getElementById("dietForm");
    const resultContainer = document.getElementById("resultContainer");
    const downloadBtn = document.getElementById("downloadBtn");
    const statsBanner = document.getElementById("statsBanner");
    let macroChartInstance = null;

    if (!dietForm) return;

    downloadBtn.addEventListener("click", () => window.print());

    dietForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Hide stats & print button while loading
        downloadBtn.classList.add("hidden");
        statsBanner.classList.add("hidden");

        const height = parseFloat(document.getElementById("height").value);
        const weight = parseFloat(document.getElementById("weight").value);
        const age = parseFloat(document.getElementById("age").value);
        const gender = document.getElementById("gender").value;
        const goal = document.getElementById("goal").value;
        const diettype = document.getElementById("diettype").value;
        const validity = document.getElementById("validity").value;

        const restrictions = Array.from(
            document.querySelectorAll('input[name="restrictions"]:checked')
        ).map(cb => cb.value);

        // Display loading UI
        resultContainer.innerHTML = `
            <div class="flex flex-col items-center justify-center py-12 text-emerald-600 gap-4">
                <i class="fa-solid fa-circle-notch fa-spin text-4xl"></i>
                <p class="font-semibold text-slate-600 text-lg">Designing custom meal plans & macro targets...</p>
            </div>
        `;

        // Calculate Macros (Mifflin-St Jeor Equation)
        let bmr = (10 * weight) + (6.25 * height) - (5 * age) + (gender === "Female" ? -161 : 5);
        let tdee = bmr * 1.375;

        if (goal === "Lose Weight") tdee -= 400;
        else if (goal === "Gain Muscle") tdee += 350;

        const calories = Math.round(tdee);
        const protein = Math.round(weight * (goal === "Gain Muscle" ? 2.0 : 1.6));
        const fats = Math.round((calories * 0.25) / 9);
        const carbs = Math.round((calories - (protein * 4) - (fats * 9)) / 4);
        const water = (weight * 0.04).toFixed(1);

        // Update Stat Cards
        document.getElementById("targetCalories").innerText = `~${calories} kcal`;
        document.getElementById("targetProtein").innerText = `~${protein}g`;
        document.getElementById("targetWater").innerText = `${water} Liters`;
        document.getElementById("targetCarbsFats").innerText = `~${carbs}g / ~${fats}g`;
        statsBanner.classList.remove("hidden");

        // Render Macro Chart
        renderChart(protein, carbs, fats);

        // Send request to Flask backend endpoint
        try {
            const response = await fetch("/api/generate-plan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ height, weight, age, gender, goal, diettype, restrictions, validity })
            });

            const data = await response.json();

            if (data.success) {
                resultContainer.innerHTML = marked.parse(data.plan);
                downloadBtn.classList.remove("hidden");
            } else {
                resultContainer.innerHTML = `<div class="p-4 bg-red-50 text-red-600 rounded-xl border border-red-200 font-bold">Error: ${data.error}</div>`;
            }
        } catch (err) {
            console.error(err);
            resultContainer.innerHTML = `<div class="p-4 bg-red-50 text-red-600 rounded-xl border border-red-200 font-bold">Connection Error: Ensure your Flask backend (app.py) is running on port 5000.</div>`;
        }
    });

    function renderChart(protein, carbs, fats) {
        const ctx = document.getElementById("macroChart").getContext("2d");
        if (macroChartInstance) macroChartInstance.destroy();

        macroChartInstance = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["Protein (g)", "Carbs (g)", "Fats (g)"],
                datasets: [{
                    data: [protein, carbs, fats],
                    backgroundColor: ["#10b981", "#a855f7", "#f59e0b"],
                    borderWidth: 2,
                    borderColor: "#ffffff"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { boxWidth: 12, font: { size: 11, weight: "bold" } }
                    }
                },
                cutout: "65%"
            }
        });
    }
});