from src.model import batch_run
import sys

if sys.argv[-1] == '--debug':
    batch_run(True)
else:
    batch_run()
