""" This file will hold the init info,
    - Mongodb Access handle
    - Authorization decorator

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 24th Feb, 2018
"""

from functools import wraps
from flask import g, request, redirect, url_for, abort
from flask_dance.contrib.github import github


def login_required(f):
    @wraps(f)
    def decorated_function( *args, **kwargs ):
        if not github.authorized:
            #return redirect( url_for("github.login", next=request.url) )
            #abort(401)
            return "<h2>You are unauthorized for this page</h2> Please go to /authorize_me<p>--manohar"
            return
        return f(*args, **kwargs )
    return decorated_function
