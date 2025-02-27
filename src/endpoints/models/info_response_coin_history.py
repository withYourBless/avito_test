from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict
from typing import Any, ClassVar, Dict, List, Optional
from .info_response_coin_history_received_inner import InfoResponseCoinHistoryReceivedInner
from .info_response_coin_history_sent_inner import InfoResponseCoinHistorySentInner
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class InfoResponseCoinHistory(BaseModel):
    """
    InfoResponseCoinHistory
    """ # noqa: E501
    received: Optional[List[InfoResponseCoinHistoryReceivedInner]] = None
    sent: Optional[List[InfoResponseCoinHistorySentInner]] = None
    __properties: ClassVar[List[str]] = ["received", "sent"]

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
        """Create an instance of InfoResponseCoinHistory from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in received (list)
        _items = []
        if self.received:
            for _item in self.received:
                if _item:
                    _items.append(_item.to_dict())
            _dict['received'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in sent (list)
        _items = []
        if self.sent:
            for _item in self.sent:
                if _item:
                    _items.append(_item.to_dict())
            _dict['sent'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of InfoResponseCoinHistory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "received": [InfoResponseCoinHistoryReceivedInner.from_dict(_item) for _item in obj.get("received")] if obj.get("received") is not None else None,
            "sent": [InfoResponseCoinHistorySentInner.from_dict(_item) for _item in obj.get("sent")] if obj.get("sent") is not None else None
        })
        return _obj


