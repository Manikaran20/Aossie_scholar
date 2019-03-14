
from django.shortcuts import render

from django.views.generic import TemplateView

from django.http import HttpResponse

from aossie_scholar.forms import IndexForm

from aossie_scholar.scrap import Scraper

from aossie_scholar.metrictables import NameTable

from .models import Author


class IndexView(TemplateView):
	template_name = 'aossie_scholar/index.html'

	def get(self, request):
		form = IndexForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = IndexForm(request.POST)
		if form.is_valid():
			text1 = form.cleaned_data['scholar_url']
			text2 = form.cleaned_data['max_approx_publications']
			scholar_data = Scraper(text1, text2)
			Author.objects.all().delete()
			b=scholar_data.f()
			table= NameTable(Author.objects.all())
			
			normalized_papers= b[0]
			total_normalized_citations=b[1]
			normalized_h_index= b[2]
			
			#for i in table:
			#	print("sandeep",i.Citations, i.CoAuthors
			#		)
			#print ('a', table)
			#Number_of_authors = b.coAuths
			#Titles= b.title_list
			#citations= b.newCitations
			#n_c= b.n_citations
			return render(request, 'aossie_scholar/metrics.html', {'Table': table, 'normalized_papers': normalized_papers,
			 'total_normalized_citations': total_normalized_citations, 'normalized_h_index': normalized_h_index} )#{'auths': Number_of_authors, 'title': Titles, 'citations': citations, 'normalized citations': n_c} )


# Create your views here.
