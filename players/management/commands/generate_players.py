import argparse
import os
import uuid

from django.core.management import BaseCommand
from django.test import RequestFactory
from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import User
from players.views import code as code_view


_AVATAR_CODES_DIRECTORY = 'players/avatar_examples'

## Code file listing

def _strip_prefix(prefix, string):
    if string.startswith(prefix):
        return string[len(prefix):]

def _get_available_code_files(base_directory):
    for dirpath, dirnames, filenames in os.walk(base_directory):
        for f in filenames:
            if not f.startswith('_') and f.endswith('.py'):
                parent_dir = _strip_prefix(base_directory, dirpath)
                yield os.path.join(parent_dir, f)

_AVATAR_CODES = list(_get_available_code_files(_AVATAR_CODES_DIRECTORY))

## Code file loading

def _load_code_file(filename):
    if not filename.endswith('.py'):
        filename = filename + '.py'

    filepath = os.path.join(_AVATAR_CODES_DIRECTORY, filename)

    with open(filepath) as f:
        return f.read()


class LoadCodeAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super(LoadCodeAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string):
        values = _load_code_file(values)
        setattr(namespace, self.dest, values)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Generate users for the game"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.engine = import_module(settings.SESSION_ENGINE)
        self.request_factory = RequestFactory()


    def add_arguments(self, parser):
        parser.add_argument('--num-users', type=int, required=True,
            help='Number of users to create')
        parser.add_argument('--avatar-code', choices=_AVATAR_CODES,
            action=LoadCodeAction, required=True,
            help='The code to use for the avatar.')


    # A command must define handle()
    def handle(self, *args, **options):
        num_users = options['num_users']
        code = options['avatar_code']

        for _ in xrange(num_users):
            random_string = str(uuid.uuid4())[:8]
            username = 'zombie-%s' % random_string
            password = '123'
            user = self.create_user(username, password)
            self.post_code(user, code)

    def create_user(self, username, password):
        user = User.objects.create_superuser(username, 'user@generated.com', password)
        self.stdout.write('Created user %s with password: %s' % (username, password))
        return user

    def post_code(self, user, player_code):
        request = self.request_factory.post('/any_path', data={'code': player_code})
        session_key = None
        request.session = self.engine.SessionStore(session_key)
        request.user = user

        response = code_view(request)
        if response.status_code == 200:
            self.stdout.write('Posted code for player %s' % user)
        else:
            raise Exception('Failed to submit code for player %s' % user)
