import re
from urllib.parse import unquote
from quart import Blueprint, render_template, request, redirect, url_for
from quart_jwt_extended import set_access_cookies

from ..database import get_session
from .. import queries as qr

auth_router = Blueprint("auth_router", __name__)


@auth_router.route("/registration", methods=["GET", "POST"])
async def registration():
    next_url = request.args.get("next", url_for("auth_router.login"))
    error_message = None

    if request.method == "POST":
        form = await request.form
        fullname = form.get("fullname")
        phone_number = form.get("phone_number")
        password = form.get("password")
        date_of_birth = form.get("date_of_birth")
        gender = form.get("gender")

        async with get_session() as session:
            token, err = await qr.registration(
                session=session,
                fullname=fullname,
                phone_number=re.sub(r'\D', '', phone_number),
                password=password,
                date_of_birth=date_of_birth,
                gender=gender,
            )

        if err:
            error_message = err
        else:
            resp = redirect(unquote(next_url))
            set_access_cookies(resp, token)
            return resp

    return await render_template(
        "registration.html", next=next_url, error_message=error_message
    )


@auth_router.route("/login", methods=["GET", "POST"])
async def login():
    next_url = request.args.get("next", url_for("main_router.index"))
    error_message = None

    if request.method == "POST":
        form = await request.form
        phone_number = form.get("phone_number")
        password = form.get("password")

        async with get_session() as session:
            token, err = await qr.login(session, phone_number, password)

        if err:
            error_message = err
        else:
            response = redirect(unquote(next_url))
            set_access_cookies(response, token)
            return response

    return await render_template(
        "login.html", next=next_url, error_message=error_message
    )
