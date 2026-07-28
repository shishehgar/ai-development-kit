# Logger

AIDK uses one central logger.

Do not use print() inside the application.

Always use:

```python
from aidk.core.logger import get_logger

log = get_logger()
