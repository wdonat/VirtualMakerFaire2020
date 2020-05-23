from flask import render_template
from . import main
import logging

@main.app_errorhandler(404)
def page_not_found(e):
    logging.info('Returned page not found')
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    logging.info('Returned internal server error')
    return render_template('500.html'), 500

