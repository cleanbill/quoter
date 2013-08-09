from django.contrib import admin
from core.models import Quote, QuoteLine, Viewing, Customer, Section, DefaultDetails, SubHeading

class QuoteAdmin(admin.ModelAdmin):
    pass

class QuoteLineAdmin(admin.ModelAdmin):
    pass

class ViewingAdmin(admin.ModelAdmin):
    pass

class CustomerAdmin(admin.ModelAdmin):
    pass

class SectionAdmin(admin.ModelAdmin):
    pass

class DefaultDetailsAdmin(admin.ModelAdmin):
    pass

class SubHeadingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Quote, QuoteAdmin)
admin.site.register(QuoteLine, QuoteLineAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Viewing, ViewingAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(DefaultDetails,DefaultDetailsAdmin)
admin.site.register(SubHeading,SubHeadingAdmin)
