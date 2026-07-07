document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('donation-form');
    const input = document.getElementById('food-input');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    
    const workflowSection = document.getElementById('workflow-section');
    
    // Triage elements
    const triageStatus = document.getElementById('status-triage');
    const triageLog = document.getElementById('triage-log');
    const triageResult = document.getElementById('triage-result');
    const stepTriage = document.getElementById('step-triage');
    
    // Logistics elements
    const logisticsStatus = document.getElementById('status-logistics');
    const logisticsLog = document.getElementById('logistics-log');
    const logisticsResult = document.getElementById('logistics-result');
    const stepLogistics = document.getElementById('step-logistics');
    const connector = document.querySelector('.step-connector');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const description = input.value.trim();
        if (!description) return;

        // Reset UI
        workflowSection.classList.remove('hidden');
        triageResult.classList.add('hidden');
        logisticsResult.classList.add('hidden');
        connector.classList.remove('active');
        
        // Button Loading State
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        submitBtn.disabled = true;

        // Animate Agent 1
        stepTriage.classList.add('active');
        triageStatus.textContent = 'Processing';
        triageStatus.className = 'status-badge processing';
        triageLog.textContent = 'Analyzing input for categorization...';

        stepLogistics.classList.remove('active');
        logisticsStatus.textContent = 'Waiting...';
        logisticsStatus.className = 'status-badge';
        logisticsLog.textContent = 'Waiting for classification...';

        try {
            // Fake delay for UI micro-animation to show processing
            await new Promise(r => setTimeout(r, 600));

            const response = await fetch('/api/process_food', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ description })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to process request');
            }

            // Success Triage Phase
            triageStatus.textContent = 'Complete';
            triageStatus.className = 'status-badge success';
            triageLog.textContent = 'Classification successful:';
            triageResult.textContent = data.food_type;
            triageResult.classList.remove('hidden');
            stepTriage.classList.remove('active');

            connector.classList.add('active');

            // Animate Agent 2
            await new Promise(r => setTimeout(r, 400));
            stepLogistics.classList.add('active');
            logisticsStatus.textContent = 'Processing';
            logisticsStatus.className = 'status-badge processing';
            logisticsLog.textContent = `Querying MCP Server for '${data.food_type}' food charities...`;
            
            await new Promise(r => setTimeout(r, 800));

            // Success Logistics Phase
            logisticsStatus.textContent = 'Complete';
            logisticsStatus.className = 'status-badge success';
            logisticsLog.textContent = 'Delivery plan generated:';
            logisticsResult.textContent = data.plan;
            logisticsResult.classList.remove('hidden');
            stepLogistics.classList.remove('active');

        } catch (error) {
            console.error(error);
            triageStatus.textContent = 'Error';
            triageStatus.className = 'status-badge';
            triageLog.textContent = error.message;
            stepTriage.classList.remove('active');
        } finally {
            // Restore Button State
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });
});
