from collections.abc import Callable
from traceback import format_exception
from typing import NoReturn, TypeVar, Generic, Optional

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E', bound=Exception)

class Result(Generic[T, E]):
    """Stores a result, with either a value or an error."""

    def __init__(self,
                 value: Optional[T] = None,
                 throwable: Optional[E] = None):
        if value is None and throwable is None:
            raise ValueError("value and throwable cannot both be none.")
        if value is not None and throwable is not None:
            raise ValueError("value and throwable cannot both be not none.")
        if throwable and not isinstance(throwable, Exception):
            raise ValueError("throwable must be an Exception")
        self.__value = value
        self.__throwable = throwable

    def peek(self, callable: Callable[[T], None]) -> 'Result[T, E]':
        try:
            callable(self.get_value())
            return self
        except Exception as e:
            return Result.of_error(e)

    def map(self, callable: Callable[[T], U]) -> 'Result[U, E]':
        if self.is_error():
            return Result.of_error(self.get_error())
        return Result.lift(lambda: callable(self.get_value()))
 
    def flat_map(self, callable: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        if self.is_error():
            return Result.of_error(self.get_error())
        return callable(self.get_value())


    def get_value(self) -> T:
        if self.is_error():
            raise self.get_error()
        if self.__value is None:
            raise Exception("Cannot retrieve value on result without value.")
        return self.__value

    def get_error(self) -> E:
        if self.is_error():
            if self.__throwable is None:
                raise Exception("Cannot retrieve error on result without error.")
            return self.__throwable
        raise Exception("Cannot retrieve error on result without error.")

    def is_error(self) -> bool:
        return self.__throwable is not None

    @staticmethod
    def lift(callable: Callable[..., U]) -> 'Result[U, E]':
        try:
            return Result.of(callable())
        except Exception as e:
            return Result.of_error(e)

    @staticmethod
    def of(value: T) -> 'Result[T, E]':
        if isinstance(value, Exception):
            return Result.of_error(value)
        return Result(value, None)

    @staticmethod
    def of_error(error: E) -> 'Result[T, E]':
        if not isinstance(error, Exception):
            return Result.of(error)
        return Result(None, error)

    def __repr__(self):
        return f"""Result(value=`{"None" if self.is_error() else self.get_value()}`, error=`{"None" if not self.is_error() else self.get_error()}`)"""

    def __str__(self):
        if self.is_error():
            return ''.join(format_exception(type(self.__throwable), self.__throwable, self.__throwable.__traceback__))
        else:
            return str(self.__value)

