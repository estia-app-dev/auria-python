import os
from abc import ABC

from auria.Enums import DevEnvironmentEnum
from auria.Exceptions import AppException
from auria.utils.TextFormatUtils import TextFormatUtils
from auria.utils.TraceUtils import TraceUtils


class Env(ABC):
  AVAILABLE_LANGUAGES = {}
  REQUIRED_VARS = [
    'E_ENV',
    'E_DEBUG',
    'E_SERVER_TOKEN',
    'E_SERVER_AES_KEY',
    'E_DB_HOST',
    'E_DB_USERNAME',
    'E_DB_PASSWORD',
    'E_DB_NAME',
    'E_DB_ECHO',
  ]

  @staticmethod
  def isEnvVarExists(envVar: str):
    if os.getenv(envVar) is None:
      raise AppException('Missing ' + envVar + ' env var')

  @staticmethod
  def checkEnvironmentVars():
    for envVar in Env.REQUIRED_VARS:
      Env.isEnvVarExists(envVar)

  @staticmethod
  def defineProjectEnvironmentVars(devEnv: DevEnvironmentEnum, debug: bool, serverToken: str, serverAesKey):
    os.environ['E_ENV'] = str(devEnv.value)
    os.environ['E_DEBUG'] = str(debug)
    os.environ['E_SERVER_TOKEN'] = serverToken  # Chaine random pour faire des actions de masse
    os.environ['E_SERVER_AES_KEY'] = serverAesKey  # Pour le cryptage des données côté server

  @staticmethod
  def defineDatabaseEnvironmentVars(host: str, dbName: str, dbUsername: str, dbPassword: str, echo: bool = False):
    os.environ['E_DB_ECHO'] = str(echo)
    os.environ['E_DB_HOST'] = host
    os.environ['E_DB_NAME'] = dbName
    os.environ['E_DB_USERNAME'] = dbUsername
    os.environ['E_DB_PASSWORD'] = dbPassword

  @staticmethod
  def defineApiEnvironmentVars(basicAuthUsername: str, basicAuthPassword: str, apiJWTSecret: str, minVersion: int):
    Env.upsertRequiredVar('E_BASIC_AUTH_USERNAME', basicAuthUsername)
    Env.upsertRequiredVar('E_BASIC_AUTH_PASSWORD', basicAuthPassword)
    Env.upsertRequiredVar('E_API_JWT_SECRET', apiJWTSecret)  # Pour l'encodage du BearerToken (voir ApiTokenManager)
    Env.upsertRequiredVar('E_API_MIN_VERSION', str(minVersion))

  @staticmethod
  def upsertRequiredVar(key: str, value):
    if key not in Env.REQUIRED_VARS:
      Env.REQUIRED_VARS.append(key)
    os.environ[key] = value

  @staticmethod
  def addLanguages(languages: dict):
    Env.AVAILABLE_LANGUAGES = languages

  ######################
  # ENVIRONMENT
  ######################

  @staticmethod
  def getEnv() -> str:
    return os.getenv('E_ENV', None)

  @staticmethod
  def debug() -> bool:
    return TextFormatUtils.strToBool(os.getenv('E_DEBUG', False))

  @staticmethod
  def getServerToken() -> str:
    return os.getenv('E_SERVER_TOKEN')

  @staticmethod
  def getServerAesKey() -> str:
    return os.getenv('E_SERVER_AES_KEY')

  ######################
  # DATABASE
  ######################

  @staticmethod
  def getDbHost() -> str:
    return os.getenv('E_DB_HOST')

  @staticmethod
  def getDbUserName() -> str:
    return os.getenv('E_DB_USERNAME')

  @staticmethod
  def getDbPassword() -> str:
    return os.getenv('E_DB_PASSWORD')

  @staticmethod
  def getDbName() -> str:
    return os.getenv('E_DB_NAME')

  @staticmethod
  def isDbEcho() -> bool:
    return TextFormatUtils.strToBool(os.getenv('E_DB_ECHO', False))

  @staticmethod
  def getDbServerURI() -> str:
    uri = 'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
    return uri.format(db_username=Env.getDbUserName(),
                      db_password=Env.getDbPassword(),
                      db_host=Env.getDbHost(),
                      db_name=Env.getDbName())

  ######################
  # API
  ######################

  @staticmethod
  def getApiBasicAuthUsername() -> str:
    return os.getenv('E_BASIC_AUTH_USERNAME', None)

  @staticmethod
  def getApiBasicAuthPassword() -> str:
    return os.getenv('E_BASIC_AUTH_PASSWORD', None)

  @staticmethod
  def getApiMinVersion() -> float:
    return float(os.getenv('E_API_MIN_VERSION', 0))

  @staticmethod
  def getApiJWTSecret() -> str:
    return os.getenv('E_API_JWT_SECRET', None)

  #######################################################
  #######################################################

  @staticmethod
  def inDevMode() -> bool:
    return Env.getEnv() == DevEnvironmentEnum.DEVELOPMENT.value

  @staticmethod
  def inProductionMode() -> bool:
    return Env.getEnv() == DevEnvironmentEnum.PRODUCTION.value

  @staticmethod
  def inTestMode() -> bool:  # Identique au mode production, mais avec des vars env locales
    return Env.getEnv() == DevEnvironmentEnum.TEST.value

  #######################################################
  #######################################################

  @staticmethod
  def trace(*args, sep=' ', end='\n', file=None):  # Todo, move or remove (voir TraceUtils.debug)
    if Env.debug():
      TraceUtils.debug(*args, sep, end, file)
