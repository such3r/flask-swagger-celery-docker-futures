from flask import Blueprint, jsonify, request

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


@bp.route('/<id>', methods=["GET"])
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
        output = {"msg": f"Getting {id}."}
        return jsonify(output)
    elif request.method == "DELETE":
        output = {"msg": f"Deleting {id}."}
        return jsonify(output)


@bp.route('/add', methods=["POST"])
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
            application/json:
              schema: MessageSchema
      tags:
          - History
    """
    # retrieve body data from input JSON
    raw = request.get_json()
    output = {"msg": f"Your data has length: '{len(raw)}'"}
    return jsonify(output)
