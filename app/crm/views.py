import uuid
from app.web.utils import json_response, check_basic_auth
from app.crm.models import User
from app.web.app import View
from aiohttp import web_exceptions
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from app.crm.schemes import UserAddSchema, ListUsersResponseSchema, UserGetSchema, UserGetResponseSchema, UserSchema
from app.web.schemes import OkResponseSchema
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden


class AddUserView(View):
    @docs(tags=["crm"], summary="add new user", description="add a new user to database")
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)     # указать статус ответ
    async def post(self):
        data = self.request["data"]
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View):
    @docs(tags=["crm"], summary="List users", description="List users from database")
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):

        if not self.request.headers.get("Authorization"):
            raise HTTPUnauthorized
        if not check_basic_auth(self.request.headers["Authorization"], username=self.request.app.config.username,
                                password=self.request.app.config.password):
            raise HTTPForbidden

        users = await self.request.app.crm_accessor.list_users()
        raw_users = [UserSchema().dump(user) for user in users]
        return json_response(data={"users": raw_users})


class GetUserView(View):
    @docs(tags=["crm"], summary="get user by id", description="add a new user to database")
    @querystring_schema(UserGetSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        user_id = self.request.query.get("id")
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={"user": UserSchema().dump(user)})  # UserSchema().dump преобразует питон в json
        raise web_exceptions.HTTPNotFound
