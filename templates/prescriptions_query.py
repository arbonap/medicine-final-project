from model import *

init_app()
# -------------------------------------------------------
# show how
test = Prescriptions.query.get(1)
print test
