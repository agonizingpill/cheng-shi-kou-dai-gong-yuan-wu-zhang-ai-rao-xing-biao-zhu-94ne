from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

class MergeTags(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    alias: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    canonical: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
