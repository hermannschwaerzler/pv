from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from datetime import datetime
import sys

from program.models import Show, TimeSlot, Note


class Command(BaseCommand):
    help = 'adds a note to a timeslot'
    args = '<show_id> <start_date> <status> [index]'

    def handle(self, *args, **options):
        if len(args) == 3:
            show_id = args[0]
            start_date = args[1]
            status = args[2]
        elif len(args) == 4:
            show_id = args[0]
            start_date = args[1]
            status = args[2]
            index = args[3]
        else:
            raise CommandError('you must provide the show_id, start_date, status [index]')

        try:
            show = Show.objects.get(id=show_id)
        except Show.DoesNotExist as dne:
            raise CommandError(dne)

        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError as ve:
            raise CommandError(ve)
        else:
            year, month, day = start.year, start.month, start.day

        try:
            timeslot = TimeSlot.objects.get(show=show, start__year=year, start__month=month, start__day=day)
        except TimeSlot.DoesNotExist as dne:
            raise CommandError(dne)
        except TimeSlot.MultipleObjectsReturned:
            if not index:
                raise CommandError('you must provide the show_id, start_date, status index')
            try:
                timeslot = \
                    TimeSlot.objects.filter(show=show, start__year=year, start__month=month, start__day=day).order_by(
                        'start')[int(index)]
            except IndexError as ie:
                raise CommandError(ie)

        try:
            title = sys.stdin.readline().rstrip()
            lines = sys.stdin.readlines()
        except Exception as e:
            raise CommandError(e)

        note = Note(timeslot=timeslot, title=title, content=''.join(lines), status=status)

        try:
            note.validate_unique()
        except ValidationError as ve:
            raise CommandError(ve.messages[0])
        else:
            note.save()
            print 'added note "%s" to "%s"' % (title, timeslot)
