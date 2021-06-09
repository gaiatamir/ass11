from flask import Blueprint, render_template
import app
# about blueprint definition
assignment10 = Blueprint('assignment10', __name__, static_folder='static', static_url_path='/assignment10', template_folder='templates')

# Routes
@assignment10.route('/assignment10')
def index():
    return render_template('assignment10.html')
