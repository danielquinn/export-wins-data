# export-wins-data

The data server component for the export-wins application

## Making the Environment Work

There are a bunch of environment variables required to run this, so I
have a little bash function that lives in my environment to automate
some common jobs:

```bash
function ew {

  cd /path/to/exportwins
  . ${HOME}/.virtualenvs/exportwins/bin/activate

  UI_SECRET='some-secret'
  DATA_SECRET='some-other-secret'
  SHARED_ARGS="DEBUG='1' UI_SECRET='secret' DATA_SERVER='http://localhost:8002' EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend' SENDING_ADDRESS='noreploy@nowhere.ca' FEEDBACK_ADDRESS='feedback@nowhere.ca'"
  PYTHON="/home/daniel/.virtualenvs/exportwins/bin/python"

  alias ui-server="SECRET_KEY='${UI_SECRET}' ${SHARED_ARGS} ${PYTHON} ./ui/manage.py runserver localhost:8001"
  alias data-server="SECRET_KEY='${DATA_SECRET}' ${SHARED_ARGS} ${PYTHON} ./data/manage.py runserver localhost:8002"

  alias ui-shell="SECRET_KEY='${UI_SECRET}' ${SHARED_ARGS} ${PYTHON} ./ui/manage.py shell_plus"
  alias data-shell="SECRET_KEY='${DATA_SECRET}' ${SHARED_ARGS} ${PYTHON} ./data/manage.py shell_plus"
  
  alias ui-test="SECRET_KEY='${UI_SECRET}' ${SHARED_ARGS} py.test ui"
  alias data-test="SECRET_KEY='${DATA_SECRET}' ${SHARED_ARGS} py.test data"

  alias ui-manage="SECRET_KEY='${UI_SECRET}' ${SHARED_ARGS} ${PYTHON} ./ui/manage.py "
  alias data-manage="SECRET_KEY='${DATA_SECRET}' ${SHARED_ARGS} ${PYTHON} ./data/manage.py "
  
}
```


## How to Run the Tests

If you're using the trick for your environment mentioned above, you just
need to run `data-test` or `ui-test`.  If not, you'll have to do
something like this:

1. Enter your virtualenv
2. Install pytest, pytest-sugar, and pytest-django.  All of these are
   already in the `requirements.txt` file.
3. Change to the root directory of this project (where `pytest.ini` 
   lives)
3. Execute `py.test`.


