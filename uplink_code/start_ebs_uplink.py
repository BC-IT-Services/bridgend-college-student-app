from pathlib import Path
from decimal import Decimal
from time import sleep
from dotenv import load_dotenv
import datetime as datetime
import os, ebs_link, anvil.server, logging, sys

load_dotenv()

UPLINK_KEY = os.environ.get('UPLINK_KEY')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

logger.info(f"Anvil uplink key from env - {UPLINK_KEY}")

connected = False

while not connected:
    try:
        logger.info(f"Connecting to Anvil server...")
        anvil.server.connect(UPLINK_KEY)
    except Exception as e:
        logger.exception(f"Anvil server failed to connect: {e}")
        logger.info("Retrying in 10 seconds...")
        sleep(60)
    else:
        connected = True
        
logger.info(f"Connected to Anvil server...")

@anvil.server.callable(require_user=True)
def get_name(person_code):
    person_code = int(anvil.users.get_user()['studentid'])
    logger.info("Calling get_name")
    return ebs_link.get_student_name(person_code=person_code)

@anvil.server.callable(require_user=True)
def get_timetable_data_lite(person_code):
    person_code = int(anvil.users.get_user()['studentid'])
    logger.info("Calling get_timetable_data_lite")   
    return ebs_link.get_student_timetable(person_code=person_code)

logger.info(f"Ready to go, waiting for requests...")

anvil.server.wait_forever()

