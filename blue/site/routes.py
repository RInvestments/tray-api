from flask import Blueprint, request
from ..config import login_required
from ..config import q_ticker

mod = Blueprint( 'site', __name__ )

@mod.route( '/' )
def index():
    return 'public page in `site`'

@mod.route( '/secret_page')
@login_required
def secret_page():
    return 'This is a secret_page in mysite'


@mod.route( '/getCompany', methods=['GET', 'POST'] )
@login_required
def getCompany():
    return 'dd:'+q_ticker.getCompanyName( '2333.HK')
