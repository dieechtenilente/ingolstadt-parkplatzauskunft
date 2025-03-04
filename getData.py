import requests
import json
from bs4 import BeautifulSoup
import argparse

# Parse Parameters

# Set up the argument parser
parser = argparse.ArgumentParser(description="Script get parking information from Ingolstadt")

# Adding the command line arguments
parser.add_argument("--username", type=str, help="Username")
parser.add_argument("--password", type=str, help="Password")
parser.add_argument("--url", type=str, help="URL")
parser.add_argument("--output_file", type=str, help="Output file")

# Parse the arguments
args = parser.parse_args()

# Access the command line arguments
username = args.username
password = args.password
url = args.url
output_file = args.output_file


headers = {"content-type" : "application/soap+xml"}
body = f"""
         <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:cfc="http://cfc_webservice">
            <soap:Header/>
            <soap:Body>
               <cfc:getParkInfoData>
                  <cfc:login>{username}</cfc:login>
                  <cfc:password>{password}</cfc:password>
               </cfc:getParkInfoData>
            </soap:Body>
         </soap:Envelope>
         """
try:
   response = requests.post(url, data = body, headers = headers)

   if (response.status_code == 200):
      content = str(response.content).replace("&lt;", "<")
      content = content.replace("\\n", "")
      content = content.replace("\\t", "")
      content = content.replace("\\xc3\\xa4", "ä")
      content = content.replace("\\xc3\\xbc", "ü")
      content = content.replace("\\xc3\\xbc", "ö")
      content = content.replace("b'<?xml version=\\'1.0\\' encoding=\\'UTF-8\\'?><soapenv:Envelope xmlns:soapenv=\"http://www.w3.org/2003/05/soap-envelope\"><soapenv:Body><ns:getParkInfoDataResponse xmlns:ns=\"http://cfc_webservice\"><ns:return>", "")
      content = content.replace("</ns:return></ns:getParkInfoDataResponse></soapenv:Body></soapenv:Envelope>'", "")
      #content is now a clean xml
      #print(content)

      content = content.replace('<?xml version="1.0" encoding="UTF-8"?>',"")
      contentXML = BeautifulSoup(content, "lxml")

      # JSON object for this query
      query = {}
      query['id'] = contentXML.find('parkinfoquery')['id']
      query['timestamp'] = contentXML.find('parkinfoquery')['timestamp']
      query = json.loads(json.dumps(query))

      parkingspots = []

      for i in contentXML.find_all('parkinfoitem'):
         name = i.find('name').get_text()
         categories = i.find('categories').get_text()
         max = i.find('max').get_text()
         free = i.find('free').get_text()
         tendency = i.find('tendency').get_text()

         data = {}
         data['name'] = str(name)
         data['categories'] = str(name)

         try:
            data['max'] = int(max)
         except ValueError:
            data['max'] = -1
         
         try:
            data['free'] = int(free)
         except ValueError:
            data['free'] = -1
         
         try:
            data['tendency'] = int(tendency)
         except ValueError:
            data['tendency'] = -1

         parkingspots.append(data)

      query['parkingspots'] = parkingspots
      #print(json.dumps(query))

      f = open(output_file, "a", encoding='utf8')
      f.write(json.dumps(query) + "\n")
      f.close()

except (requests.exceptions.SSLError, TypeError, TimeoutError, requests.exceptions.ConnectionError) as e:
   response = None