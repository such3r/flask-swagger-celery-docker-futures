"""Flask Application"""

# load libaries
from flask import Flask, jsonify
from flask_dropzone import Dropzone

# load modules
from src.endpoints.history import bp as history
from src.endpoints.graph import bp as graph
from src.endpoints.swagger import swagger_ui_blueprint, SWAGGER_URL

# init Flask app
app = Flask(__name__)

app.config.update(
    # Flask-Dropzone config:
    DROPZONE_MAX_FILE_SIZE=100,  # set max size limit to a large number, here is 100 MB
    DROPZONE_TIMEOUT=1 * 60 * 1000,  # set upload timeout to a large number, here is 1 minute
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.csv, .xls, .xlsx', # set allowed file types to known tabular
    DROPZONE_REDIRECT_VIEW='graph.main_view',
)

dropzone = Dropzone(app)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(history, url_prefix="/api/v1/history")
app.register_blueprint(graph, url_prefix="/api/v1/graph")

from src.api_spec import spec
# register all swagger documented functions here

with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)

@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
