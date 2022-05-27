from flask import Blueprint, jsonify, request

history_blueprint_name: str = "history"
history = Blueprint(name=history_blueprint_name, import_name=__name__)

@history.route('/test', methods=['GET'])
def test():
    """
    ---
    get:
      description: test endpoint
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: MessageSchema
      tags:
          - testing
    """
    output = {"msg": f"I'm the test endpoint from {history_blueprint_name}."}
    return jsonify(output)


@history.route('/get/<id>')
def get_history(id: str):
    """
    ---
    get:
      description: gets history file
      parameters:
      - in: path
        schema: FileIDSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: MessageSchema
      tags:
          - calculation
    """
    output = {"msg": f"Getting {id}."}
    return jsonify(output)


@history.route('/manage', methods=["POST", "DELETE"])
def manage_history():
    """
    ---
    post:
      description: adds the new file to the database
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
          - calculation
    delete:
      description: removes the file by ID from the database
      requestBody:
        required: true
        content:
            application/json:
                schema: FileIDSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: MessageSchema
      tags:
          - calculation
    """
    if request.method == "POST":
        # retrieve body data from input JSON
        raw = request.get_json()
        output = {"msg": f"Your data has length: '{len(raw)}'"}
        return jsonify(output)
    elif request.method == "DELETE":
        id = request.get_json()
        output = {"msg": f"DELETE history at {id}"}
        return jsonify(output)
