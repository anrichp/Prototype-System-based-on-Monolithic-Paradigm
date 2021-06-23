"""
Dashboard
"""
from flask import render_template
from Application.dashboard import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
