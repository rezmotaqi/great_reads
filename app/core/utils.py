from motor.motor_asyncio import AsyncIOMotorDatabase


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


def return_app_instance():
    from app.main import app

    return app


# noinspection PyUnresolvedReferences
def mongo_db() -> AsyncIOMotorDatabase:
    app = return_app_instance()
    return app.state.mongo_db
