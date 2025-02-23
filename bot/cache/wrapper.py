class FieldWrapper:
    """
    Обёртка над одним конкретным значением,
    позволяющая читать его как строку/число,
    и вызывать `await .set(...) / .del(...)` для обновления в Redis.
    """
    def __init__(self, parent, field_name: str, default=None):
        """
        :param parent: ссылка на родителя (Settings, Profile, или сам UserCache),
                       откуда мы можем дотянуться до redis и user_id
        :param field_name: название поля (например, "language")
        :param default: значение по умолчанию, если ничего не нашлось
        """
        self._parent = parent
        self._field_name = field_name
        self._default = default

    def get_value(self):
        return self._parent._data.get(self._field_name, self._default)

    async def set(self, value):
        self._parent._data[self._field_name] = value
        await self._parent._save_field(self._field_name, value)

    def __str__(self):
        val = self.get_value()
        return str(val) if val is not None else ""

    def __repr__(self):
        return repr(self.get_value())

    def __eq__(self, other):
        val = self.get_value()
        if isinstance(other, FieldWrapper):
            return val == other.get_value()
        return val == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return bool(self.get_value())