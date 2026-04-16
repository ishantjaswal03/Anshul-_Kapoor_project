document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const btn = document.getElementById('analyze-btn');
    const resultsPanel = document.getElementById('results-panel');
    const statusIcon = document.getElementById('status-icon');
    const statusText = document.getElementById('status-text');
    const probabilityValue = document.getElementById('probability-value');
    const probabilityBar = document.getElementById('probability-bar');
    const anomalyValue = document.getElementById('anomaly-value');
    
    // Set loading state
    btn.classList.add('loading');
    btn.disabled = true;

    // Gather data
    const data = {
        machine_id: form.machine_id.value,
        temperature: parseFloat(form.temperature.value),
        vibration: parseFloat(form.vibration.value),
        pressure: parseFloat(form.pressure.value),
        rpm: parseFloat(form.rpm.value),
        power_consumption: parseFloat(form.power_consumption.value),
        cycle_count: parseInt(form.cycle_count.value),
        operating_hours: parseInt(form.operating_hours.value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === 'success') {
            // Apply reveal classes
            resultsPanel.classList.add('revealed');
            
            // Clear old status
            document.querySelector('.status-indicator').classList.remove('status-healthy', 'status-critical');

            if (result.failure_likely) {
                document.querySelector('.status-indicator').classList.add('status-critical');
                statusText.innerText = "Critical Failure Risk";
            } else {
                document.querySelector('.status-indicator').classList.add('status-healthy');
                statusText.innerText = "Machine Operating Nominally";
            }

            // Update Metrics
            const probPercent = (result.failure_probability * 100).toFixed(1);
            probabilityValue.innerText = `${probPercent}%`;
            probabilityBar.style.width = `${probPercent}%`;
            
            // Adjust bar color based on percentage by updating background mapping dynamically
            if (probPercent > 70) {
                probabilityBar.style.background = "var(--accent-red)";
            } else if (probPercent > 30) {
                probabilityBar.style.background = "#eab308"; // warning yellow
            } else {
                probabilityBar.style.background = "var(--accent-green)";
            }

            anomalyValue.innerText = result.anomaly_detected ? "Detected" : "None";
            anomalyValue.style.color = result.anomaly_detected ? "var(--accent-red)" : "var(--accent-green)";
        } else {
            alert("Error: " + result.message);
        }

    } catch (error) {
        console.error("Prediction error:", error);
        alert("Failed to connect to AI engine.");
    } finally {
        // Remove loading state
        btn.classList.remove('loading');
        btn.disabled = false;
    }
});
