import re

from django.core.exceptions import ValidationError


def validate_title_is_hexa_code(name: str) -> None:
    """Валидация значения как HEX-кода.

    Args:
        name: Цветовой HEX-код.

    Raises:
        ValidationError: Если `name` не соответствует шаблону.
    """

    regex = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    pattern = re.compile(regex)

    if not name or not re.search(pattern, name):
        raise ValidationError(
            '%(value)s должен быть цветовым HEX-кодом',
            params={'value': name},
        )
