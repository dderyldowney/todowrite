# Python 3.12+ Typing Standards

## 🎯 Mandatory Requirements (Updated 2025-11-26)

### Core Principles
- **ALL Python files MUST use `from __future__ import annotations`**
- **NO `Any` types allowed** - use specific types or `Protocol`
- **Full type coverage** on all functions, variables, and returns
- **Maximum 500 lines per file**

### 🚀 Python 3.12+ New Features (PEP 695)

#### 1. Type Parameter Syntax
```python
# OLD way (pre-Python 3.12)
from typing import TypeVar, Generic
T = TypeVar('T')

class Container(Generic[T]):
    def method(self, item: T) -> T: ...

# NEW way (Python 3.12+)
class Container[T]:
    def method(self, item: T) -> T: ...

def func[T](a: T) -> T: ...
```

#### 2. Type Statement for Aliases
```python
# OLD way
Vector = list[float]

# NEW way (Python 3.12+)
type Vector = list[float]
type ListOrSet[T] = list[T] | set[T]
```

#### 3. Type Variable Tuples
```python
def move_first_element_to_last[T, *Ts](tup: tuple[T, *Ts]) -> tuple[*Ts, T]:
    return tup[1:] + (tup[0],)
```

#### 4. Automatic Variance Inference
- No more manual variance specification
- Python 3.12+ infers variance automatically

### 📋 Modern Type Requirements

#### Built-in Generics (No typing module imports needed)
```python
# Use built-in generics
names: list[str] = []
scores: dict[str, int] = {}
items: set[str] = set()

# Instead of typing module
# from typing import List, Dict, Set  # ❌ Don't use
```

#### Union Operator
```python
# Use | operator
result: str | int | None

# Instead of Union
# from typing import Union, Optional  # ❌ Don't use
# result: Union[str, int] | Optional[None]  # ❌ Don't use
```

#### Advanced Types
```python
# Final for constants
MAX_CONNECTIONS: Final[int] = 100

# Never for unreachable code
def raise_error() -> Never:
    raise ValueError("Always fails")

# TypeGuard for type narrowing
def is_str(val: object) -> TypeGuard[str]:
    return isinstance(val, str)

# Protocol for structural typing
class Drawable:
    def draw(self) -> None: ...
```

### 🔧 Migration Checklist

For every Python file:
1. ✅ Add `from __future__ import annotations` at top
2. ✅ Replace `List[str]` with `list[str]`
3. ✅ Replace `Union[str, int]` with `str | int`
4. ✅ Replace `Optional[str]` with `str | None`
5. ✅ Replace `Dict[str, int]` with `dict[str, int]`
6. ✅ Remove all `Any` types
7. ✅ Use new `type` statements for aliases
8. ✅ Use type parameter syntax for generics

### 📚 References
- [Python 3.12 typing documentation](https://docs.python.org/3.12/library/typing.html)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [Context7 for up-to-date examples](https://context7.com)

---
*Last updated: 2025-11-26 via systematic debugging and Context7 research*
