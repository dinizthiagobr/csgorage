#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Thiago Diniz Maia
# dinizthiagobr@gmail.com
#

import cfscrape
import requests
import re
import json
import time
from bs4 import BeautifulSoup
from random import randint

def writeToFile(text) :
	f = open('r.html', 'w')
	f.write(text)
	f.close()

rafflesDone = []

while True :
	raffleUrl = "a"	
	cookies = dict('...')

	scraper = cfscrape.create_scraper()
	scraper.get("http://www.csgorage.com")
	r = scraper.get("http://www.csgorage.com/free-raffles", cookies=cookies)	

	if (r.status_code != 200) :
		continue

	s = BeautifulSoup(r.text, "html.parser")

	raffles = s.findAll('div', attrs={'class':'raffle_box_lg white_gradient'})
	if (raffles == -1) :
		continue	

	for r in raffles:
		button = r.find('button')
		raffleType = button.find('span')
		raffleType = str(raffleType)
		if "Lvl 5" not in raffleType:
			raffles.remove(r)
 	
	for r in raffles:
		raffle_pageRef = r.find('a', href=re.compile('^/raffle/'))
		if (raffle_pageRef == -1) :
			continue

		raffle_pageLink = raffle_pageRef['href']
		raffleUrl = "http://www.csgorage.com" + raffle_pageLink
		if (raffleUrl in rafflesDone) :
			continue

		print("New raffle :)")
	
		headers = { 'Host' : 'csgorage.com',
        	    'Connection' : 'keep-alive',
		        'Referer' : 'http://csgorage.com/free-raffles',
	            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	            'Upgrade-Insecure-Requests' : '1',
	            'Accept-Encoding' : 'gzip, deflate, sdch',
	            'Accept-Language' : 'en-US,en;q=0.8,pt;q=0.6,es;q=0.4'              
	         }

		r = scraper.get(raffleUrl, cookies=cookies)

		if (r.status_code != 200) :
			continue

		s = BeautifulSoup(r.text, "html.parser")
		token = s.find('span', attrs={'class':'hide tok'}).contents[1]
		if (token == -1) :
			continue
		token = str(token)[6:-7]
	
		rid = raffleUrl.split('-')[-1] 
		
		headers = { 'Host' : 'csgorage.com',
		        'Origin' : 'http://csgorage.com',
	            'Referer' : raffleUrl,
	            'Connection' : 'keep-alive',
	            'Accept' : 'application/json, text/javascript, */*; q=0.01',
	            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
	            'Accept-Encoding' : 'gzip, deflate',
	            'Accept-Language' : 'en-US,en;q=0.8,pt;q=0.6,es;q=0.4'
        	 }
	
		payload = { 'rid' : rid, 'last' : 960, '_token' : token }
		url = "http://www.csgorage.com/slots"
	
		r = scraper.post(url, cookies=cookies, data=payload, headers=headers)

		if (r.status_code != 200) :
			continue
	
		rJson = json.loads(r.text)

		ticketId = randint(962, 1430)
		
		while (str(ticketId) in rJson) :
			print(". . .")
			ticketId = randint(962, 1430)
	
		url = "http://www.csgorage.com/getslotfree"
		payload = { 'rid' : rid, 'slots[]' : ticketId , '_token' : token }

		r = scraper.post(url, cookies=cookies, data=payload, headers=headers)
		if (r.status_code == 200) :
			rJson = json.loads(r.text)
			if (rJson['r']) : 
				print("Ticket for " + raffleUrl + " : " + str(ticketId) + " : OK")
				rafflesDone.append(raffleUrl)
		else :
			writeToFile(r.status_code)
			f = open('r.html', 'a')
			f.write("\n\n" + r.text)
			f.close
	
	time.sleep(600)

