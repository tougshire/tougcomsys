from datetime import date, timedelta
from django.test import TestCase

from tougcomsys.models import Placement, ICal 
from tougcomsys.views import events_from_icals, events_from_articles, combine_event_dicts


class TestEventsFromIcals(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.placement = Placement.objects.create(
            title="Test",
            place_number=1,
            type=0,
            event_list_start=0,
            events_list_length=465,
            )
        
        cls.ical = ICal.objects.create(
            name='Test',
            url='https://calendar.google.com/calendar/ical/c_6c014c01b653827e5176890fbfea60d4d5396cc1729ad6fca0c093a68c98cc4c%40group.calendar.google.com/public/basic.ics',
            placement=Placement.objects.first()
        )

    def test_events_from_icals( self ):
        first_dict = events_from_icals( self.placement )
        second_dict = events_from_articles( self.placement )
        events = combine_event_dicts( first_dict, second_dict )

        print(events)
