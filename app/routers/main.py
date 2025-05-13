from quart import Blueprint, render_template, redirect, url_for
from quart_jwt_extended import verify_jwt_in_request_optional, get_jwt_identity

from ..database import get_session
from ..queries import get_user_by_id

main_router = Blueprint("main_router", __name__)

@main_router.route("/")
async def index():
    await verify_jwt_in_request_optional()
    user_id = get_jwt_identity()

    if not user_id:
        return redirect(url_for("auth_router.login"))

    async with get_session() as session:
        user = await get_user_by_id(session, user_id)

    full_name = f"{user.surname} {user.name} {user.patronymic or ''}".strip()
    return await render_template("welcome.html", full_name=full_name)