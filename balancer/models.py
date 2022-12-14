from typing import List, Union

import validators
import json
from pydantic import BaseModel, validator


class BalancerParams(BaseModel):
    video: Union[List[str], str]

    @validator('video')
    def video_url_validation(cls, v) -> str:
        if not validators.url(v[0], public=True):
            raise ValueError('video url not validated')
        return v[0]


class CDNConfig(BaseModel):
    location: str
    settings: Union[dict, str]

    @validator('settings')
    def settings_validation(cls, v) -> dict:
        if isinstance(v, str):
            return json.loads(v)
        return v
