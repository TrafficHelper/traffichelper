# coding: utf-8

"""
    Traffic Wise

    This is the API for traffic wise based on OpenAPI 3.0 specification..

    The version of the OpenAPI document: 1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import pprint
import re  # noqa: F401
import json


from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from openapi_server.models.safe_routes_path_choices import SafeRoutesPathChoices
from openapi_server.models.safe_routes_start_end import SafeRoutesStartEnd
from openapi_server.models.safe_routes_start_time import SafeRoutesStartTime
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class SafeRoutes(BaseModel):
    """
    SafeRoutes
    """ # noqa: E501
    start_end: Optional[SafeRoutesStartEnd] = Field(default=None, alias="StartEnd")
    start_time: Optional[SafeRoutesStartTime] = Field(default=None, alias="StartTime")
    environment: Optional[StrictStr] = 'Normal'
    path_choices: Optional[SafeRoutesPathChoices] = Field(default=None, alias="PathChoices")
    path_count: Optional[Union[Annotated[float, Field(le=5, strict=True, ge=0)], Annotated[int, Field(le=5, strict=True, ge=0)]]] = None
    __properties: ClassVar[List[str]] = ["StartEnd", "StartTime", "environment", "PathChoices", "path_count"]

    @field_validator('environment')
    def environment_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Ideal', 'Normal', 'Abnormal', 'Deviant', 'Troublesome', 'Extreme'):
            raise ValueError("must be one of enum values ('Ideal', 'Normal', 'Abnormal', 'Deviant', 'Troublesome', 'Extreme')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of SafeRoutes from backend.a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from backend.calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from backend.pydantic by calling `to_dict()` of start_end
        if self.start_end:
            _dict['StartEnd'] = self.start_end.to_dict()
        # override the default output from backend.pydantic by calling `to_dict()` of start_time
        if self.start_time:
            _dict['StartTime'] = self.start_time.to_dict()
        # override the default output from backend.pydantic by calling `to_dict()` of path_choices
        if self.path_choices:
            _dict['PathChoices'] = self.path_choices.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of SafeRoutes from backend.a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "StartEnd": SafeRoutesStartEnd.from_dict(obj.get("StartEnd")) if obj.get("StartEnd") is not None else None,
            "StartTime": SafeRoutesStartTime.from_dict(obj.get("StartTime")) if obj.get("StartTime") is not None else None,
            "environment": obj.get("environment") if obj.get("environment") is not None else 'Normal',
            "PathChoices": SafeRoutesPathChoices.from_dict(obj.get("PathChoices")) if obj.get("PathChoices") is not None else None,
            "path_count": obj.get("path_count")
        })
        return _obj


