#This file is part galatea_file blueprint for Flask.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from flask import Blueprint, Response, abort, current_app
from galatea.tryton import tryton
from mimetypes import guess_type

galatea_file = Blueprint('galatea_file', __name__, template_folder='templates')

Attachment = tryton.pool.get('ir.attachment')

RESOURCE = current_app.config.get('TRYTON_ATTACHMENT_RESOURCE')

@galatea_file.route('/file/<filename>', endpoint="file")
@tryton.transaction()
def filename(filename):

    attachments = Attachment.search([
        ('name', '=', filename),
        ], limit=1)
    if not attachments:
        abort(404)
    attachment, = attachments
    resource = str(attachment.resource)
    if not resource.split(',')[0] in RESOURCE:
        abort(404)

    file_mime = guess_type(filename)[0]
 
    return Response(attachment.data, mimetype=file_mime)
