from aossie_scholar.models import Author
import bs4
import urllib.request
from bs4 import BeautifulSoup as soup 
from selenium import webdriver
import time
import re



title_list = []
Citations =[]
coAuths = []
n_citations = []
newCitations = []
N_author_url= []
author_names_list= []
url_to_counter= []
number_of_coauths=[]


class Scraper():

	def __init__(self, url, maxP):

		self.url= url

		self.maxP = maxP

	def f(self):

		for i in range(0,1000,100):

			if (int(self.maxP.encode('utf-8'))<=i):
				pageSize = i
				break

		n_papers= 0                      #to count normalized papers.
		sum_citations= 0  
		counter = 0   
		ncounter = 0
		acounter= 0
		bcounter= 0            # to count total numbers citations an author recieved. 

	#{ looping trough pages to get all the publications
		for j in range(0,pageSize, 100):

			S_url=self.url + "&cstart=" + str(j) +"&pagesize=100"

			with urllib.request.urlopen(S_url) as my_url:

				page_html = my_url.read()
			
			page_soup = soup(page_html, "html.parser")

			if (j == 0):
				Name= page_soup.find('div', {'id': 'gs_prf_in'})


			aTag = page_soup.findAll('td', {'class': 'gsc_rsb_std'})

			Titles = page_soup.findAll('td', {'class': 'gsc_a_t'})

			Citations_soup = page_soup.findAll('td', {'class': 'gsc_a_c'})

			Years = page_soup.findAll('td', {'class': 'gsc_a_y'})

			info_page = page_soup.findAll('a', {'class' : 'gsc_a_at'})

			authors_soup= page_soup.findAll('div', {'class': 'gs_gray'})

		#{ loop to get all the pop up urls and then collect number of co-authors from there
			for author in info_page:

				Author_names_link = author["data-href"]

				user=Author_names_link[53:65]


				n_input=Author_names_link[-12:]

				n_author_url="https://scholar.google.com.au/citations?user="+user+"&hl=en#d=gs_md_cita-d&u=%2Fcitations%3Fview_op%3Dview_citation%26hl%3Den%26user%3D"+user+"%26citation_for_view%3D"+user+"%3A"+n_input+"%26tzom%3D-330"
				N_author_url.append(n_author_url)

			less_authors_name=[]
			for a in authors_soup:
				less_authors_name.append(a.text)

			for i in range(0, len(less_authors_name), 2):
				author_names_list.append(less_authors_name[i])


			for title in Titles:
				Title = title.a.text
				x=Title.encode('utf-8')
				title_list.append(x.decode('utf-8', 'ignore'))
				#title_list has all the titles
			
			for c in Citations_soup:
				p= c.text.encode('utf-8')
				r=p.decode('utf-8', 'ignore')
				q= re.findall('[0-9]+',r)
				Citations.append(q)

		n_author_names_list= []

		for j in author_names_list:
			if '...' not in j:
				n_author_names_list.append(author_names_list[counter])
				counter+=1
				continue
			else:
				n_author_names_list.append('#')
				url_to_counter.append(counter)
				counter+= 1

		if len(url_to_counter) != 0:
			driver= webdriver.Firefox()
			driver.implicitly_wait(0.5)
			for url in url_to_counter:
				print (url)
				#if (ncounter > 0):
				#time.sleep(0.5)
				print (N_author_url[url])
				driver.get(N_author_url[url])
				time.sleep(0.5)
				title= driver.find_elements_by_xpath('//div[@class="gsc_vcd_value"]')
				page_element = title[0].text
				print (page_element)
				coAuths.append(len(page_element.split(',')))
				ncounter+= 1
			driver.quit()

		for name in n_author_names_list:
			if (name=='#'):
				number_of_coauths.append(coAuths[acounter])
				acounter+=1
			else:
				number_of_coauths.append(len(name.split(',')))

		for entry in Citations:
			try:
				newCitations.append(entry[0])
			except:
				newCitations.append(0)
					#newCitations has all the citations as a list



		
		for element in range(len(title_list)):
			n_papers +=1/number_of_coauths[element]

			n_citations.append(int(int(newCitations[element])/number_of_coauths[element]))

		for k in newCitations:
			try:
				sum_citations+= int(k[0])
			except:
				continue

		#print ('a', title_list)
		#print('b', newCitations)
		#print('c', number_of_coauths)
		#print('d', n_citations)
		#print('e', int(n_papers))
		#print('f', int(sum(n_citations)))
		#print('g', int(sum(n_citations)/ len(title_list)))


		
		for entity in range(len(title_list)):
			a= Author(Title_name= title_list[entity], Citations=newCitations[entity], 
				CoAuthors= number_of_coauths[entity], Normalized_citations= n_citations[entity]
				)
			a.save()

		normalized_papers= int(n_papers)
		total_normalized_citations= int(sum(n_citations))
		normalized_h_index= int(sum(n_citations)/len(title_list))

		return (normalized_papers, total_normalized_citations, normalized_h_index)
		#table= [title_list, number_of_coauths, newCitations, n_citations]

				#'n_papers': int(n_papers),
				#'total_normalized_citations': int(sum(n_citations)),
				#'normalized_h-indx': int(sum(n_citations)/len(title_list)),
				#'list': range(len(title_list))
			
				#}
		#PageView= NameTable(table)
		
	#collection= len(title_list)

		#print (table)


		#print (T_citations)
		#print (n_papers)
		#print (n_citations)
		#return ('a')
		


	#setattr(f, 'normalized_papers', normalized_papers)
	#setattr(f, 'total_normalized_citations', total_normalized_citations)
	#setattr(f, 'normalized_h_index', normalized_h_index)
	#setattr(f, 'n_citations', n_citations)



	
		
