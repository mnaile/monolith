from flask_env import MetaFlaskEnv
import os

class BaseSettings(MetaFlaskEnv):
    SECRET_KEY = os.urandom(32)