from os import remove, system
from os.path import exists
from datetime import datetime
import pandas as pd
import zipfile
import Data

class App:

	def __init__(self, dataService):
		self.df = None
		self.dfs = []
		self.fileList = dataService.fetchfiles()

		if self.fileList is None:
			raise Exception("No data available!")
		else:
			for fn in self.fileList:
				if exists(fn):
					with zipfile.ZipFile(fn) as myzip:
						myzip.extract('data.csv')
						self.dfs.append(pd.read_csv('data.csv'))
						remove('data.csv')
			self.df = pd.concat(self.dfs, ignore_index=True)


	def build_email_report(self):
		query = ~self.df['Outbound'].isnull() & ~(self.df['Outbound'] == 'internal')
		emails = self.df.loc[query, 'Outbound'].drop_duplicates()
		report = []

		for email in emails:
			query = (self.df['Outbound'] == email)
			a = self.df.loc[query, ['PURL', 'Event', 'Outbound']].drop_duplicates()
			date = [datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p') for x in self.df.loc[query, 'Date']]
			date.sort()
			date = date[0].strftime('%m/%d/%Y')
			counts = a['Event'].value_counts()

			report.append({
				'email': email,
				'date': date,
				'recipients': counts.get('Email sent to Contact', 0),
				'opened': counts.get('Contact opened Email', 0),
				'clicked': counts.get('Contact clicked a link in Email', 0),
				'unsubscribed': counts.get('Contact opted-out of Email', 0),
				'hardbounced': counts.get('Email hard bounced', 0),
				'softbounced': counts.get('Email soft bounced', 0),
				'suppressed': counts.get('Suppressed', 0),
				'openrate': (counts.get('Contact opened Email', 0) / counts.get('Email sent to Contact', 0)) * 100,
				'clickrate': (counts.get('Contact clicked a link in Email', 0) / counts.get('Email sent to Contact', 0)) * 100
			})

		return sorted(report, key = lambda i: i['date'])


	def build_microsite_report(self):
		# Microsite_Events:
		# Contact visited Microsite
		# Contact Visited Page
		# Contact provided form data
		# Contact Submitted Page
		# Contact added a new Contact
		# Contact clicked an outside link
		# New Contact added to database

		series_visited = self.df['Event'].str.contains('visit', case=False)
		series_formsubmit = self.df['Event'].str.contains('submit', case=False)
		series_linkclicks = self.df['Event'].str.contains('outside link', case=False)
		series_referal = self.df['Event'].str.contains('database')

		b2c = self.df['Inbound'].str.contains('Reason')
		b2b = self.df['Inbound'].str.contains('b2b')
		refer = self.df['Inbound'].str.contains('Refer')

		b2c_frame_visited = self.df.loc[series_visited & b2c, 'Contact_ID'].drop_duplicates()
		b2c_frame_formsubmit = self.df.loc[series_formsubmit & b2c, 'Contact_ID'].drop_duplicates()
		b2c_frame_linkclicks = self.df.loc[series_linkclicks & b2c, 'Contact_ID'].drop_duplicates()

		b2b_frame_visited = self.df.loc[series_visited & b2b, 'Contact_ID'].drop_duplicates()
		b2b_frame_formsubmit = self.df.loc[series_formsubmit & b2b, 'Contact_ID'].drop_duplicates()
		b2b_frame_linkclicks = self.df.loc[series_linkclicks & b2b, 'Contact_ID'].drop_duplicates()

		refer_frame_visited = self.df.loc[series_visited & refer, 'Contact_ID'].drop_duplicates()
		refer_frame_formsubmit = self.df.loc[series_formsubmit & refer, 'Contact_ID'].drop_duplicates()
		refer_frame_linkclicks = self.df.loc[series_linkclicks & refer, 'Contact_ID'].drop_duplicates()

		print(self.df.loc[series_formsubmit & refer, 'PURL'].drop_duplicates())


		return {
			'b2c': {
				'visits': len(b2c_frame_visited),
				'form_responses': len(b2c_frame_formsubmit),
				'links': len(b2c_frame_linkclicks)
			},
			'b2b': {
				'visits': len(b2b_frame_visited),
				'form_responses': len(b2b_frame_formsubmit),
				'links': len(b2b_frame_linkclicks)
			},
			'refer': {
				'visits': len(refer_frame_visited),
				'form_responses': len(refer_frame_formsubmit),
				'links': len(refer_frame_linkclicks)
			}
		}
