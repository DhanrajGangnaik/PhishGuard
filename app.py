from flask import Flask, render_template, request
from utils.db import init_db, insert_scan, get_counts, get_recent_scans, get_chart_data
from utils.predictor import analyze_input

app = Flask(__name__)
init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    counts = get_counts()
    recent_scans = get_recent_scans(limit=5)

    if request.method == 'POST':
        input_type = request.form.get('input_type', 'url')
        content = request.form.get('content', '').strip()

        if not content:
            return render_template(
                'index.html',
                error='Please enter a URL or email content.',
                counts=counts,
                recent_scans=recent_scans,
            )

        result = analyze_input(input_type, content)
        insert_scan(
            input_type=input_type,
            content=content,
            label=result['label'],
            score=result['score'],
            reasons=result['reasons'],
        )
        return render_template('result.html', result=result)

    return render_template('index.html', counts=counts, recent_scans=recent_scans)


@app.route('/dashboard')
def dashboard():
    counts = get_counts()
    recent_scans = get_recent_scans(limit=10)
    chart_data = get_chart_data()
    return render_template(
        'dashboard.html',
        counts=counts,
        recent_scans=recent_scans,
        chart_data=chart_data,
    )


@app.route('/history')
def history():
    recent_scans = get_recent_scans(limit=50)
    return render_template('history.html', recent_scans=recent_scans)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
