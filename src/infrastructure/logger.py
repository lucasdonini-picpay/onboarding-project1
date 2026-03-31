from uvicorn.logging import DefaultFormatter
import logging, sys

logger = logging.getLogger("onboarding-proj1")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

formatter = DefaultFormatter(fmt="%(levelprefix)s %(message)s", use_colors=True)

handler.setFormatter(formatter)
logger.addHandler(handler)
