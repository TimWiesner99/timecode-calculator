document.addEventListener('DOMContentLoaded', function() {
    const calculateBtn = document.getElementById('calculateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const timecodesInput = document.getElementById('timecodes');
    const framerateSelect = document.getElementById('framerate');
    const framerateGroup = document.getElementById('framerateGroup');
    const resultDiv = document.getElementById('result');
    const resultValue = document.getElementById('resultValue');
    const errorDiv = document.getElementById('error');
    const subtitle = document.getElementById('subtitle');
    const hint = document.getElementById('hint');
    const exampleList = document.getElementById('exampleList');
    const modeBtns = document.querySelectorAll('.mode-btn');

    let currentMode = 'frames';

    const modeConfig = {
        frames: {
            subtitle: 'Add timecodes in HH:MM:SS:FF format',
            placeholder: '00:00:10:00\n00:00:15:12\n00:01:05:08',
            hint: 'Format: HH:MM:SS:FF — paste timecodes from Excel, one per line',
            examples: [
                ['00:00:10:00', '10 seconds'],
                ['00:01:30:12', '1 minute, 30 seconds, 12 frames'],
                ['01:15:45:23', '1 hour, 15 minutes, 45 seconds, 23 frames'],
            ],
            showFramerate: true,
        },
        decimal: {
            subtitle: 'Add timecodes in HH:MM:SS,mmm format',
            placeholder: '00:00:10,000\n00:00:15,500\n00:01:05,080',
            hint: 'Format: HH:MM:SS,mmm (milliseconds) — as used in SRT subtitle files',
            examples: [
                ['00:00:10,000', '10 seconds'],
                ['00:01:30,500', '1 minute, 30.5 seconds'],
                ['01:15:45,250', '1 hour, 15 minutes, 45.25 seconds'],
            ],
            showFramerate: false,
        },
        simple: {
            subtitle: 'Add timecodes in HH:MM:SS format',
            placeholder: '00:00:10\n00:00:15\n00:01:05',
            hint: 'Format: HH:MM:SS — hours, minutes, and seconds only',
            examples: [
                ['00:00:10', '10 seconds'],
                ['00:01:30', '1 minute, 30 seconds'],
                ['01:15:45', '1 hour, 15 minutes, 45 seconds'],
            ],
            showFramerate: false,
        },
    };

    function setMode(mode) {
        currentMode = mode;
        const config = modeConfig[mode];

        subtitle.textContent = config.subtitle;
        timecodesInput.placeholder = config.placeholder;
        hint.textContent = config.hint;
        framerateGroup.classList.toggle('hidden', !config.showFramerate);
        exampleList.innerHTML = config.examples
            .map(([tc, desc]) => `<li><code>${tc}</code> — ${desc}</li>`)
            .join('');

        modeBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        timecodesInput.value = '';
    }

    modeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            setMode(this.dataset.mode);
        });
    });

    calculateBtn.addEventListener('click', calculateSum);
    copyBtn.addEventListener('click', copyToClipboard);

    // Allow Ctrl+Enter to calculate
    timecodesInput.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            calculateSum();
        }
    });

    async function calculateSum() {
        const timecodes = timecodesInput.value;
        const framerate = parseFloat(framerateSelect.value);

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
                    mode: currentMode,
                    framerate: framerate,
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
