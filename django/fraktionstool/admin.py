from django.contrib import admin
from fraktionstool.models import GremiumTyp, Gremium, VorhabenTyp
from fraktionstool.models import Vorhaben, Nachricht, GremiumVorhaben

class GremienInline(admin.TabularInline):
	model = GremiumVorhaben
	extra = 1

class VorhabenAdmin(admin.ModelAdmin):
	inlines = (GremienInline,)

admin.site.register(GremiumTyp)
admin.site.register(Gremium)
admin.site.register(VorhabenTyp)
admin.site.register(Vorhaben, VorhabenAdmin)
admin.site.register(Nachricht)
