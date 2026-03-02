from pydantic import BaseModel, Field

from .components import MetablockComponent
from .utils import compact_dict


# Extension
class Extension(BaseModel):
    """Object representing an Extension"""

    id: str = Field(description="The unique identifier of the extension")
    name: str = Field(description="The name of the extension")
    docs: str = Field(description="The documentation URL of the extension")
    org_id: str = Field(description="The organization id of the extension")
    org_name: str = Field(description="The organization name of the extension")
    schema_: dict = Field(description="The schema of the extension", alias="schema")


class Extensions(MetablockComponent):
    """Extensions"""

    async def get_list(self, *, cursor: str | None = None) -> list[Extension]:
        data = await self.cli.get(self.url, params=compact_dict(cursor=cursor))
        return [Extension(**e) for e in data]
