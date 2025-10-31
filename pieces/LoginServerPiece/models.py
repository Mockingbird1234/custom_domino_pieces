from pydantic import BaseModel, Field
from enum import Enum


class AuthMethodType(str, Enum):
    """
    Authentication method types
    """
    password = "password"
    key = "key"


class InputModel(BaseModel):
    base64_bytes_data: str = Field(
        description="从上游传递的base64编码数据（通常是图片数据）",
        json_schema_extra={
            "from_upstream": "always"
        }
    )
    server_ip: str = Field(
        description="服务器IP地址"
    )
    port: int = Field(
        default=22,
        description="SSH端口号"
    )
    username: str = Field(
        description="用户名"
    )
    password: str = Field(
        description="密码",
        json_schema_extra={
            "widget": "password"
        }
    )
    auth_method: AuthMethodType = Field(
        default=AuthMethodType.password,
        description="认证方法：password(密码认证)、key(密钥认证)"
    )
    private_key_path: str = Field(
        default="",
        description="私钥文件路径（密钥认证时使用）"
    )
    connection_timeout: int = Field(
        default=30,
        description="连接超时时间（秒）"
    )


class OutputModel(BaseModel):
    login_success: bool = Field(
        description="登录是否成功"
    )
    connection_id: str = Field(
        description="SSH连接标识符"
    )
    server_info: str = Field(
        description="服务器连接信息"
    )
    server_hostname: str = Field(
        description="服务器主机名"
    )
    server_os: str = Field(
        description="服务器操作系统信息"
    )
    base64_bytes_data: str = Field(
        description="传递的base64编码数据"
    )