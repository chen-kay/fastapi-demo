from pydantic import BaseModel, Field

# class LoginParam(BaseModel):
#     username: str = Field(None, title='用户名')
#     password: str = Field(None, title='密码')


class LoginType(BaseModel):
    status: str = Field("error", title="状态")
    message: str = Field(None, title="错误信息")
    access_token: str = Field(None, title="jwt access_token")
    token_type: str = Field(None, title="jwt token type")
