from flask import Blueprint, jsonify, render_template, make_response
from ..utils import plot_graph_from_id

blueprint_name: str = "graph"
bp = Blueprint(name=blueprint_name, import_name=__name__)

@bp.route('/test', methods=['GET'])
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
          - Testing
    """
    output = {"msg": f"I'm the test endpoint from {blueprint_name}."}
    return jsonify(output)


# @bp.route('/', methods=['GET'])
# def get_graph():
#     """
#     ---
#     get:
#       description: Main page for graph drawing
#       parameters:
#       - in: ID
#         schema: FileIDSchema
#       responses:
#         '200':
#           description: call successful
#           content:
#             text/html:
#               schema: MessageSchema
#       tags:
#           - Visualization
#     """
#     graph_json = plot_graph_from_id(id)
#     return make_response(render_template('graph.html', graphJSON=graph_json))


@bp.route('/<id>', methods=['GET'])
def get_graph(id: str):
    """
    ---
    get:
      description: Draws graph from the history file by ID
      parameters:
      - in: ID
        schema: FileIDSchema
      responses:
        '200':
          description: call successful
          content:
            text/html:
              schema: MessageSchema
      tags:
          - Visualization
    """
    graph_json = plot_graph_from_id(id)
    return make_response(render_template('graph.html', graphJSON=graph_json))
