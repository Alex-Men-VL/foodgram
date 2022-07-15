import pydantic


class Ingredient(pydantic.BaseModel):
    title: str = pydantic.Field(alias='name')
    unit: str = pydantic.Field(alias='measurement_unit')

    class Config:
        validate_assignment = True
        extra = pydantic.Extra.forbid
