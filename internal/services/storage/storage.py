from internal.repositories.store import Store


class Storage:
    def __init__(self, store: Store) -> None:
        self.__store = store

    def create(self):
        try:
            self.__store.create()
        except Exception as err:
            raise err
