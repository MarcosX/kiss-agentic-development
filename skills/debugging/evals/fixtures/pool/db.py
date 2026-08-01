class ConnectionPool:
    def __init__(self, max_conns=3):
        self.max_conns = max_conns
        self._checked_out = 0

    def acquire(self):
        if self._checked_out >= self.max_conns:
            raise RuntimeError(f"connection pool exhausted: max {self.max_conns} connections")
        self._checked_out += 1
        return object()

    def release(self, conn):
        self._checked_out -= 1
