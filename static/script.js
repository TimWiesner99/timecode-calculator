document.addEventListener('DOMContentLoaded', function() {
    const calculateBtn = document.getElementById('calculateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const timecodesInput = document.getElementById('timecodes');
    const framerateSelect = document.getElementById('framerate');
    const resultDiv = document.getElementById('result');
    const resultValue = document.getElementById('resultValue');
    const errorDiv = document.getElementById('error');

    calculateBtn.addEventListener('click', calculateSum);
    copyBtn.addEventListener('click', copyToClipboard);

    // Allow Enter key to calculate (with Ctrl/Cmd)
    timecodesInput.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            calculateSum();
        }
    });

    async function calculateSum() {
        const timecodes = timecodesInput.value;
        const framerate = parseFloat(framerateSelect.value);

        // Hide previous results/errors
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');

        if (!timecodes.trim()) {
            showError('Please enter at least one timecode');
            return;
        }

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    timecodes: timecodes,
                    framerate: framerate
                })
            });

            const data = await response.json();

            if (response.ok) {
                showResult(data.result);
            } else {
                showError(data.error || 'An error occurred');
            }
        } catch (error) {
            showError('Failed to connect to server: ' + error.message);
        }
    }

    function showResult(result) {
        resultValue.textContent = result;
        resultDiv.classList.remove('hidden');
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    function copyToClipboard() {
        const text = resultValue.textContent;

        navigator.clipboard.writeText(text).then(function() {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            copyBtn.style.background = '#28a745';
            copyBtn.style.color = 'white';

            setTimeout(function() {
                copyBtn.textContent = originalText;
                copyBtn.style.background = '';
                copyBtn.style.color = '';
            }, 2000);
        }).catch(function(err) {
            showError('Failed to copy to clipboard');
        });
    }
});
