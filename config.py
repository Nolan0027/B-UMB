import os

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise ValueError("The TOKEN environment variable is not set!")
