from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from .info_response_coin_history import InfoResponseCoinHistory
from .info_response_inventory_inner import InfoResponseInventoryInner
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class InfoResponse(BaseModel):
    """
    InfoResponse
    """ # noqa: E501
    coins: Optional[StrictInt] = Field(default=None, description="Количество доступных монет.")
    inventory: Optional[List[InfoResponseInventoryInner]] = None
    coin_history: Optional[InfoResponseCoinHistory] = Field(default=None, alias="coinHistory")
    __properties: ClassVar[List[str]] = ["coins", "inventory", "coinHistory"]

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
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of InfoResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
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
        # override the default output from pydantic by calling `to_dict()` of each item in inventory (list)
        _items = []
        if self.inventory:
            for _item in self.inventory:
                if _item:
                    _items.append(_item.to_dict())
            _dict['inventory'] = _items
        # override the default output from pydantic by calling `to_dict()` of coin_history
        if self.coin_history:
            _dict['coinHistory'] = self.coin_history.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of InfoResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "coins": obj.get("coins"),
            "inventory": [InfoResponseInventoryInner.from_dict(_item) for _item in obj.get("inventory")] if obj.get("inventory") is not None else None,
            "coinHistory": InfoResponseCoinHistory.from_dict(obj.get("coinHistory")) if obj.get("coinHistory") is not None else None
        })
        return _obj


