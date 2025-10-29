from pydantic import BaseModel, Field
from enum import Enum


class OutputTypeType(str, Enum):
    """
    Output type for the result text
    """
    file = "file"
    base64_string = "base64_string"
    both = "both"


class InputModel(BaseModel):
    input_image: str = Field(
        description='输入图像。它应该是文件路径，或是 base64 编码的字符串。',
        json_schema_extra={
            "from_upstream": "always"
        }
    )
    sepia: bool = Field(
        default=False,
        description='应用棕褐色效果。',
    )
    black_and_white: bool = Field(
        default=False,
        description='应用黑白效果。',
    )
    brightness: bool = Field(
        default=False,
        description='应用亮度效果。',
    )
    darkness: bool = Field(
        default=False,
        description='应用黑暗效果。',
    )
    contrast: bool = Field(
        default=False,
        description='应用对比效果。',
    )
    red: bool = Field(
        default=False,
        description='应用红色效果。',
    )
    green: bool = Field(
        default=False,
        description='应用绿色效果。',
    )
    blue: bool = Field(
        default=False,
        description='应用蓝色效果。',
    )
    cool: bool = Field(
        default=False,
        description='应用冷色效果。',
    )
    warm: bool = Field(
        default=False,
        description='应用暖色效果。',
    )
    output_type: OutputTypeType = Field(
        default=OutputTypeType.both,
        description='输出图像的格式。可选项为：`file`、`base64_string`、`both`。',
    )


class OutputModel(BaseModel):
    image_base64_string: str = Field(
        default='',
        description='输出图像的 Base64 编码字符串。',
    )
    image_file_path: str = Field(
        default='',
        description='输出图像文件的路径。',
    )