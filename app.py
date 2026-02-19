"""
Flask web application for timecode calculator.
"""

from flask import Flask, render_template, request, jsonify
from timecode import add_timecodes

app = Flask(__name__)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate the sum of timecodes.

    Expects JSON with:
        - timecodes: string with newline-separated timecodes
        - mode: 'frames', 'decimal', or 'simple'
        - framerate: numeric framerate (only used in 'frames' mode)

    Returns:
        JSON with result or error message
    """
    try:
        data = request.get_json()
        timecodes = data.get('timecodes', '')
        mode = data.get('mode', 'frames')
        framerate = round(float(data.get('framerate', 25)))

        if not timecodes.strip():
            return jsonify({'error': 'Please enter at least one timecode'}), 400

        result = add_timecodes(timecodes, mode=mode, framerate=framerate)
        return jsonify({'result': result})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
