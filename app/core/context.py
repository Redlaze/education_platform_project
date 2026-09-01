import contextvars
from uuid import UUID


request_id_var: contextvars.ContextVar[UUID | None] = contextvars.ContextVar(
    'request_id',
    default=None,
)


def get_request_id() -> UUID | None:
    """Возвращает request_id."""

    return request_id_var.get()


def set_request_id(request_id: UUID | None) -> None:
    """Устанавливает request_id"""

    request_id_var.set(request_id)
