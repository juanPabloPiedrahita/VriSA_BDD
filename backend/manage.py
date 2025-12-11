#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script initializes the Django environment and delegates command-line
operations to Django’s management system. It is responsible for tasks such as:
- Running the development server
- Applying migrations
- Creating superusers
- Managing apps and database interactions

The main() function sets the required settings module and then executes the
command provided through the command line.
"""
import os
import sys


def main():
    """
    Initialize Django's command-line environment and execute management commands.

    This function configures the project's settings module and then invokes
    Django's command-line utility. If Django is not installed or cannot be
    imported, an ImportError is raised with a descriptive message.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it is installed and available "
            "on your PYTHONPATH environment variable. You may also need to "
            "activate a virtual environment."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
