from django.db import models

class Customer(models.Model):
    name           = models.TextField()
    address        = models.TextField()
    postcode       = models.TextField(max_length=10)
    email          = models.EmailField()
    data           = models.TextField(null=True,blank=True)
    first_inserted = models.DateTimeField(auto_now_add=True)
    last_updated   = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name+" "+self.postcode

class Quote(models.Model):
    token          = models.TextField(unique=True)
    display        = models.BooleanField(default=True)
    title          = models.TextField()
    customer       = models.ForeignKey(Customer)
    expire         = models.DateTimeField()
    message        = models.TextField(null=True,blank=True)
    data           = models.TextField(null=True,blank=True)
    first_inserted = models.DateTimeField(auto_now_add=True)
    last_updated   = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title+" - "+self.customer.name+" ("+str(self.first_inserted)+")"

class Section(models.Model):
    order          = models.IntegerField()
    name           = models.TextField()
    total          = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.name

class Section(models.Model):
    order          = models.IntegerField()
    name           = models.TextField()
    total          = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.name

class SubHeading(models.Model):
    name           = models.TextField()

    def __unicode__(self):
        return "%s" % self.name

class DefaultDetails(models.Model):
    name           = models.TextField()

    def __unicode__(self):
        return "%s" % self.name
    
class QuoteLine(models.Model):
    order          = models.IntegerField()
    section        = models.ForeignKey(Section,null=True,blank=True)
    quote          = models.ForeignKey(Quote)
    subtitle       = models.ForeignKey(SubHeading,null=True,blank=True)
    defaultDetails = models.ForeignKey(DefaultDetails,null=True,blank=True)
    details        = models.TextField(null=True,blank=True)
    amount         = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
    data           = models.TextField(null=True,blank=True)
    first_inserted = models.DateTimeField(auto_now_add=True)
    last_updated   = models.DateTimeField(auto_now=True)

    #class Meta:
    #    detail = ('details', 'defaultDetails',)
    
    def __unicode__(self):
        return "%s %s %s " %(self.quote, self.details, self.amount)

class Viewing(models.Model):
    ip             = models.TextField()
    quote          = models.TextField()    
    data           = models.TextField(null=True,blank=True)
    first_inserted = models.DateTimeField(auto_now_add=True)
    last_updated   = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s %s" % (self.quote,self.ip,self.first_inserted)
