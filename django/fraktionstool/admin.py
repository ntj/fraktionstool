from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from fraktionstool.models import GremiumTyp, Gremium, VorhabenTyp
from fraktionstool.models import Vorhaben, Nachricht, GremiumVorhaben
from fraktionstool.models import GremiumUser

class GremienVorhabenInline(admin.TabularInline):
	model = GremiumVorhaben
	extra = 1

class VorhabenAdmin(admin.ModelAdmin):
	inlines = (GremienVorhabenInline,)
	search_fields = ('name', 'nummer')
	list_display = ('name', 'nummer', 'beobachten', 'geschlossen')

class GremienUsersInline(admin.TabularInline):
	model = GremiumUser
	extra = 1

class GremiumAdmin(admin.ModelAdmin):
	inlines = (GremienUsersInline,)

class CustomUserAdmin(UserAdmin):
	inlines = (GremienUsersInline,)

admin.site.register(GremiumTyp)
admin.site.register(Gremium, GremiumAdmin)
admin.site.register(VorhabenTyp)
admin.site.register(Vorhaben, VorhabenAdmin)
admin.site.register(Nachricht)

# Replace UserAdmin view with custom view
admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
