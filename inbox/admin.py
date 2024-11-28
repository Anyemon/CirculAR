from django.contrib import admin
from .models import *

# Register your models here.
'''
class MensajeInboxAdmin(admin.ModelAdmin):
    readonly_fields = ('remitente', 'conversacion', 'cuerpo')

admin.site.register(MensajeInbox, MensajeInboxAdmin)
admin.site.register(Conversacion)
'''
admin.site.register(MensajeInbox)
admin.site.register(Conversacion)
