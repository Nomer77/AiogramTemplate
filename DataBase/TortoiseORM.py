from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError, ConfigurationError
from typing import Final 
import logging
import sys

class ORM:
    TORTOISE_ORM: Final = Tortoise()

    @classmethod
    async def orm_init(cls) -> None:
        try:
            await cls.TORTOISE_ORM.init(
                    db_url='sqlite://db.sqlite3',
                    modules={'models': ['DataBase.models']}
                )
            await cls.TORTOISE_ORM.generate_schemas()
            logging.info("TORTOISE:TORTOISE-ORM connected.")
        except ConfigurationError as ConfigurationException:
            logging.critical(f"TORTOISE:The configuration of the ORM is invalid. {ConfigurationException}")
            sys.exit(1)
        except DBConnectionError:
            logging.critical("TORTOISE:Unable to connect to database.")
            sys.exit(1)
    
    @classmethod
    async def orm_shutdown(cls) -> None:
        logging.info("TORTOISE:TORTOISE-ORM goodbye.")
        await cls.TORTOISE_ORM.close_connections()
