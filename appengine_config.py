"""`appengine_config` gets loaded when starting a new application instance."""
from google.appengine.ext import vendor
import os
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
