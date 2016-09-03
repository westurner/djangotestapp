
from django.core.management.base import BaseCommand, CommandError

from djangotestapp.testapp.factories import main

class Command(BaseCommand):
    help = 'Do factories'

    # def add_arguments(self, parser):
    #     parser.add_argument("factory callable str", nargs="+")

    def handle(self, *args, **kwargs):
        result = main()
        if result != 0:
            raise CommandError(result)

        self.stdout.write(self.style.SUCCESS(result))
        self.stdout.write(self.style.SUCCESS('Factories completed'))
