from django.shortcuts import render
from .models import Book
from app import App
import Data
import re

# Create your views here.

dataService = Data.FtpService.getInstance(Data.creds['ftp'])
app = App(dataService)
dataStore = {
	'outbounds': app.build_email_report(),
	'inbounds': app.build_microsite_report()
}

def index(request):
	data = {
		'outbounds': list(filter(lambda a: (re.search("^(?!Email \d+).*", a['email'])), dataStore['outbounds'])),
		'inbounds': dataStore['inbounds']
	}
	
	return render(request, 'index.html', {'data': data})


def refer(request):
	data = {
		'outbounds': list(filter(lambda a: (re.search('^Email \d+', a['email'])), dataStore['outbounds'])),
		'inbounds': dataStore['inbounds']['refer']
	}
	print(data['inbounds'])
	return render(request, 'refer.html', {'data': data})


def giveaway(request):
	return render(request, 'giveaway.html', {})


def book_by_id(request, book_id):
	book = Book.objects.get(pk=book_id)
	return render(request, 'book_details.html', {'book': book})