#
#    This file is part of Quoter
#
#    Quoter is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with Quoter.  If not, see <http://www.gnu.org/licenses/>.
#
from django.http                import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts           import render_to_response, redirect
from django.contrib.auth.models import User

from core.models import *
from datetime import date, timedelta 
import datetime
from django.utils import timezone
import logging

from django.core import serializers
import json

from django.core import serializers
from django.utils import simplejson

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Block():
        pass

def totalSection(quoteLines,section):
    list = []    
    total = 0
    order = 0
    totalSection = True
    for line in quoteLines:
        if line.section.name == section:
            totalSection = line.section.total
            if line.amount:
                total = total + line.amount
            order = line.section.order
            list.append(line)
    block = Block()
    block.name = section
    block.totalSection = totalSection
    block.order = order 
    block.lines = sorted(list,key=lambda line: line.order)
    block.total = total
    return block

class GrandTotal():
        pass

def getDateBlock(quote):
    block = Block()
    block.name = "Date:"
    block.totalSection = False
    block.order = 0
    line = QuoteLine()
    line.details= quote.first_inserted
    block.lines = [line]
    block.default = True
    block.date = True
    return block
    
def getClientBlock(quote):
    block = Block()
    block.name = "Client:"
    block.totalSection = False
    block.order = 0
    line = QuoteLine()
    line.details= quote.customer.name
    block.lines = [line]
    block.default = True
    return block

def printQuote(request,quote_token):
    return quote(request,quote_token,True)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip        

def toggle(request,quote_token):    
        # Check if valid
        if (Quote.objects.filter(token=quote_token).count() == 0):
            logger.info("'%s' cannot be found in database" % quote_token)
            raise Http404
        
        # serve quote
        quoteHeader = Quote.objects.get(token=quote_token)
        quoteHeader.display = not quoteHeader.display
        quoteHeader.save()

        if quoteHeader.display:
            return quote(request,quote_token)
        else:
            logger.info("'%s' is NOW set to not display" % quote_token)
            raise Http404


def jumpin(request):
        return redirect('/admin/')
            
def nowhere(request):
        params = {}
        return render_to_response('404.html',params)

def error(request,quote_token,printFormat=False):
        view = Viewing()
        view.quote = quote_token
        view.ip    = get_client_ip(request)
        view.data  = "%s" % request
        view.save()
        
        # Check if valid
        if (Quote.objects.filter(token=quote_token).count() == 0):
            logger.info("'%s' cannot be found in database" % quote_token)
            #raise Http404
            return nowhere(request)
        
        # serve quote
        quoteHeader = Quote.objects.get(token=quote_token)
        if (not quoteHeader.display):
            logger.info("'%s' is set to not display" % quote_token)
            #raise Http404
            return nowhere(request)
        return
        
def edit(request,quote_token,printFormat=False):
        err = error(request,quote_token,printFormat=False)
        if err: return err        
        quoteHeader = Quote.objects.get(token=quote_token)
        quoteLines  = QuoteLine.objects.filter(quote=quoteHeader).order_by( 'section' )
        customers   = Customer.objects.all()#.values_list('name')
        subopts     = SubHeading.objects.all()
        sectops     = Section.objects.all()
        #detailops   = QuoteLine.objects.all().values('details').distinct()
        #print "details are %s" % detailops
        allCust     = customers#simplejson.dumps(list(customers))#serializers.serialize("json",[customers])
        blocks = []
        name = ""
        grandTotal = 0
        totals = {}
        for line in quoteLines:
            if line.defaultDetails:
                line.details = line.defaultDetails    
            if line.amount:
                grandTotal = grandTotal + line.amount
                totalName = line.subtitle.name
                if totalName in totals:
                    total = totals[totalName]
                    total = total + line.amount
                    totals[totalName] = total
                else:
                    totals[totalName] = line.amount
            if line.section.name != name:
                  blocks.append(totalSection(quoteLines,line.section.name))
                  name = line.section.name  
        blocks = sorted(blocks,key=lambda block: block.order)
        blocks.insert(0,getClientBlock(quoteHeader))
        blocks.insert(0,getDateBlock(quoteHeader))
        params = {'token':quote_token,
                  'quote':quoteHeader,
                  'customer':quoteHeader.customer,
                  'blocks': blocks,
                  'totals':totals,
                  'expireDate':"%s"%quoteHeader.expire, #.strftime('%d/%M/%Y'),
                  'total':grandTotal,
                  'subopts':subopts,
        # 'detailops':detailops,
                  'sectops':sectops,
                  'custs':customers}
        print params
        #print json.dumps(params)
        return render_to_response('edit.html',params)

def alter(request,quote_token):
        sectops  = Section.objects.all()
        subopts  = SubHeading.objects.all()

        params   = {'sectops':sectops,'subopts':subopts}
        return render_to_response('change.html',params)

def quote(request,quote_token,printFormat=False):
        err = error(request,quote_token,printFormat=False)
        if err: return err        
        # serve quote
        quoteHeader = Quote.objects.get(token=quote_token)
        if (not quoteHeader.display):
            logger.info("'%s' is set to not display" % quote_token)
            #raise Http404
            return nowhere(request)

        # Check if expired
        expireDate  = quoteHeader.expire
        today       = timezone.now()
        delta       = expireDate - today
        expired     = delta <= timedelta(minutes = 1)
        if expired: 
             logger.info("%s has expired" % quote_token) 
        else: 
             logger.info("%s is still relevent" % quote_token) 
           
        quoteLines  = QuoteLine.objects.filter(quote=quoteHeader).order_by( 'section' )
        blocks = []
        name = ""
        grandTotal = 0
        totals = {}
        for line in quoteLines:
            if line.defaultDetails:
                line.details = line.defaultDetails    
            if line.amount:
                grandTotal = grandTotal + line.amount
                totalName = line.subtitle.name
                if totalName in totals:
                    total = totals[totalName]
                    total = total + line.amount
                    totals[totalName] = total
                else:
                    totals[totalName] = line.amount
            if line.section.name != name:
                  blocks.append(totalSection(quoteLines,line.section.name))
                  name = line.section.name  
        blocks = sorted(blocks,key=lambda block: block.order)
        blocks.insert(0,getClientBlock(quoteHeader))
        blocks.insert(0,getDateBlock(quoteHeader))
        params = {'token':quote_token,
                  'quote':quoteHeader,
                  'customer':quoteHeader.customer,
                  'blocks':blocks,
                  'totals':totals,
                  'total':grandTotal,
                  'expired':expired,
                  'print':printFormat}
        return render_to_response('index.html',params)
        
