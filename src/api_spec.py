"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Create an APISpec
spec = APISpec(
    title="My App",
    version="1.0.0",
    openapi_version="3.0.3",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Define schemas
class FileIDSchema(Schema):
    id = fields.Str(description="A file ID.", required=True)

class FileInputSchema(Schema):
    file = fields.Raw(description="A file.", metadata={"type": "string", "format": "binary"}, required=True)

class MessageSchema(Schema):
    msg = fields.String(description="A message.", required=True)

# register schemas with spec
spec.components.schema("FileID", schema=FileIDSchema)
spec.components.schema("FileInput", schema=FileInputSchema)
spec.components.schema("Message", schema=MessageSchema)

# add swagger tags that are used for endpoint annotation
tags = [
            {'name': 'Testing',
             'description': 'For testing the API.'
            },
            {'name': 'History',
             'description': 'History file manipulationa.'
            },
            {'name': 'Visualization',
             'description': 'Graph depiction.'
            },
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
