from marshmallow import fields, validate
from app.extensions import ma  # Import the Marshmallow instance


class AssistanceRequestSchema(ma.Schema):
    topic = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["sales", "pricing"], error="Topic must be 'sales' or 'pricing'"
        ),
        error_messages={"required": "Topic is required."},
    )
    description = fields.Str(
        required=True, error_messages={"required": "Description is required."}
    )


class NotificationResponseSchema(ma.Schema):
    message = fields.Str(required=True)
