from flask import Blueprint, jsonify, render_template, make_response, request
from celery.result import AsyncResult
from ..utils import read_file_with_hash, add_file_to_database, read_history_by_id, remove_history_by_id

blueprint_name: str = "history"
bp = Blueprint(name=blueprint_name, import_name=__name__)

@bp.route('/test', methods=['GET'])
def test():
    """
    ---
    get:
      description: Test endpoint
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: MessageSchema
      tags:
          - Testing
    """
    output = {"msg": f"I'm the test endpoint from {blueprint_name}."}
    return jsonify(output)


@bp.route('/<id>', methods=["GET", "DELETE"])
def get_history(id: str):
    """
    ---
    get:
      description: Gets the history file by ID
      parameters:
      - in: ID
        schema: FileIDSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: MessageSchema
      tags:
          - History
    delete:
      description: Removes the file by ID from the database
      parameters:
      - in: ID
        schema: FileIDSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: MessageSchema
      tags:
          - History
    """
    if request.method == "GET":
        history = read_history_by_id(id)

        if history is None:
            output = {"history": None}
        else:
            output = {"history": history.to_json()}

        return jsonify(output)
    elif request.method == "DELETE":
        remove_history_by_id.apply_async(args=[id])
        output = {"msg": f"Deleted {id}."}
        return jsonify(output)


@bp.route('/', methods=["GET", "POST"])
def add_history():
    """
    ---
    post:
      description: Adds the new file to the database
      requestBody:
        required: true
        content:
            application/octet-stream:
                schema: FileInputSchema
      responses:
        '200':
          description: call successful
          content:
            text/html:
              schema: MessageSchema
      tags:
          - History
    """
    if request.method == 'POST':
        f = request.files.get('file')
        file_hash, contents = read_file_with_hash(f)
        add_file_to_database(file_hash, contents)#.apply_async(args=[file_hash, contents])

        # mongodb_client.save_file(f.filename, f)
        # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

    return make_response(render_template('upload.html'))
