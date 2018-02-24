from flask import Blueprint, request
from ..config import login_required

mod = Blueprint( 'site', __name__ )

@mod.route( '/' )
def index():
    return 'public page in `site`'

@mod.route( '/secret_page')
@login_required
def secret_page():
    return 'This is a secret_page in mysite'

@mod.route( '/get', methods=['GET', 'POST'] )
@login_required
def get():
    return 'dd:<pre>'+str(request)+'</pre>'
