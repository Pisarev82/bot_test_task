from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str

    def camel_to_snake(name: str) -> str:
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('_')
            result.append(char.lower())
        return ''.join(result)

    class Config:
        alias_generator = lambda s: s.camel_to_snake()
        allow_population_by_field_name = True
        # Для сериализации в snake_case:
        json_encoders = {str: lambda v: v.camel_to_snake()}
        json_by_alias = True
