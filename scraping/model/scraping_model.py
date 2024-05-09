from typing import List, Optional
from pydantic import BaseModel

from scraping.utils import data


class ScrapingDataRequest(BaseModel):
    actor_id: Optional[List[str]]
    demandado_id: Optional[List[str]]

    class Config:
        json_schema_extra = data
