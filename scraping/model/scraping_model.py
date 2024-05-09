from typing import List, Union

from pydantic import BaseModel

from scraping.utils import data


class ScrapingDataRequest(BaseModel):
    actor_id: List[Union[str, None]] = None
    demandado_id: List[Union[str, None]] = None

    class Config:
        json_schema_extra = data
