# import gspread
# from gspread_formatting import *
# from oauth2client.service_account import ServiceAccountCredentials
# scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.__scope)
# wb = gspread.authorize(self.__creds).open('Seeds')

import ftplib
import abc

creds = {
	"ftp": {
		"host": "54.210.225.180",
		"usr": "ray",
		"pwd": "Frontier2021!"
	}
}

class DataService(abc.ABC):
	@abc.abstractmethod
	def __fetchfiles__(self):
		pass


class FtpService(DataService):
	__instance = None

	@staticmethod
	def getInstance(creds):
		if FtpService.__instance == None:
			FtpService(creds)

		return FtpService.__instance


	def __init__(self, creds):
		self.ftpfiles = []
		self.__creds = creds

		if FtpService.__instance != None:
			raise Exception("FtpServer class is a singleton")
		else:
			FtpService.__instance = self


	def __fetchfiles__(self):
		ftp = ftplib.FTP(self.__creds["host"], self.__creds["usr"], self.__creds["pwd"])
		ftp.encoding = 'utf-8'
		ftp.retrlines('NLST', lambda x: self.ftpfiles.append(x) if x[-3:] == 'zip' else None)

		if len(self.ftpfiles) > 0:
			return self.ftpfiles
		else:
			return None
	
	
	def fetchfiles(self):
		return self.__fetchfiles__()
