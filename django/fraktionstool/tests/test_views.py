from django.test import TestCase
from django.test.client import Client, RequestFactory

from django.contrib.auth.models import User

from fraktionstool.models import Nachricht, Vorhaben, Gremium, GremiumTyp
from fraktionstool.models import VorhabenTyp, GremiumUser, GremiumVorhaben
from fraktionstool.views import NachrichtenList

class NachrichtenListViewTest(TestCase):
    """ Tests for the NachrichtenList view class. """

    def test_messages_in_context_request_factory(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = NachrichtenList.as_view()(request)

        self.assertEquals(list(response.context_data['object_list']), [])

        u = User.objects.create(username="test", password="testpw")
        gt = GremiumTyp.objects.create(name="Testtyp")
        g = Gremium.objects.create(name="Testgremium", typ=gt)
        gu = GremiumUser.objects.create(gremium=g, user=u)
        vt = VorhabenTyp.objects.create(name="Testvorhabentyp")
        v = Vorhaben.objects.create(name="Testvorhaben", nummer="T1",
            typ=vt)
        vg = GremiumVorhaben.objects.create(gremium=g, vorhaben=v)
        n = Nachricht.objects.create(text="Test", owner=u, vorhaben=v,
            gremium=g)

        response = NachrichtenList.as_view()(request)

        self.assertEquals(response.context_data['object_list'].count(), 1)
