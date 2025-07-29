from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
from app.models.role import Role
from app.models.official import Official
from app.models.batch import Batch
from app.models.training import Training
from app.models.training_history import TrainingHistory
from app.models.batch_tracking import BatchTracking
from app.models.log import Log