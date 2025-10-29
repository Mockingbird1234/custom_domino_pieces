from pydantic import BaseModel, Field
from enum import Enum


class MethodTypes(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class InputModel(BaseModel):
    url: str = Field(
        description="数据请求地址"
    )
    method: MethodTypes = Field(
        default=MethodTypes.GET,
        description="请求方法"
    )
    bearer_token: str = Field(
        default=None,
        description="用于认证的Token"
    )
    body_json_data: str = Field(
        default="""{
    "key_1": "value_1",
    "key_2": "value_2"
}
""",
        description="要在请求正文中发送的 JSON 数据。",
        json_schema_extra={
            'widget': "codeeditor-json",
        }
    )


class OutputModel(BaseModel):
    base64_bytes_data: str = Field(
        description='将输出数据编码为 Base64 字符串。'
    )