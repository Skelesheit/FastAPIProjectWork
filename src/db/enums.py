from enum import StrEnum

from sqlalchemy.dialects.postgresql import ENUM


class UserType(StrEnum):
    Individual = 'Физ. лицо'
    LegalEntity = 'ИП'
    LegalEntityProfile = 'Юр. лицо'

user_type_postgres = ENUM('ИП', 'Юр. лицо', 'Физ. лицо', name='user_type_enum')