# NTI Backend

## Alembic guide

При добавлении в базу новых сущностей или изменения уже существующих нужно сделать 3 шага:
### Добавить/Поменять определения в коде.
Было:
```python
class User(PostgresBase):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    roles = Column(
        ARRAY(String), nullable=False, default=list()
    )
```
Стало:
```python
# src/schemas/users.py
class Role(Enum):
    ADMIN = "admin"

class User(PostgresBase):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    roles: list[str] = Column(ARRAY(PgEnum(Role, create_type=True)), nullable=False, default=list())

# src/schemas/log_entry.py
class LogEntry(PostgresBase):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    note: Mapped[str] = mapped_column()
```
То есть меняем код прямо в сурсах.
### Автосгенерировать миграцию.
```bash
poetry run alembic revision --autogenerate -m "change Role to Enum and add LogEntry table"
```
Файлик со сгенерированной миграцией автоматически добавится в `alembic/versions/`.
### Перезапустить контейнер.
```bash
docker compose up backend
```
При старте контейнера будет вызвано `poetry run alembic upgrade head`, что и приведёт к миграции в базе.