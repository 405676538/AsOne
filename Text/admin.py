from django.contrib import admin

# Register your models here.
from Text.models import Test, UserInfo, Contact,UpLoadFile,Music


class ContactAdmin(admin.ModelAdmin):
    fields = ('name', 'email')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Test)
admin.site.register(UserInfo)
admin.site.register(UpLoadFile)
admin.site.register(Music)