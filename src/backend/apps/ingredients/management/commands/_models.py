import pydantic


class Ingredient(pydantic.BaseModel):
    name: str
    measurement_unit: str

    class Config:
        validate_assignment = True
        extra = pydantic.Extra.forbid
