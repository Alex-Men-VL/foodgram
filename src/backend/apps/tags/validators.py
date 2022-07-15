import re

from django.core.exceptions import ValidationError


def validate_title_is_hexa_code(title: str) -> None:
    """Валидация значения как HEX-кода.

    Args:
        title: Цветовой HEX-код.

    Raises:
        ValidationError: Если `title` не соответствует шаблону.
    """

    regex = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    pattern = re.compile(regex)

    if not title or not re.search(pattern, title):
        raise ValidationError(
            '%(value)s должен быть цветовым HEX-кодом',
            params={'value': title},
        )
