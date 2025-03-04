import requests
import json
from bs4 import BeautifulSoup
import config

url = config.url
output_file = config.output_file

headers = {"content-type" : "application/soap+xml"}
body = f"""
         <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:cfc="http://cfc_webservice">
            <soap:Header/>
            <soap:Body>
               <cfc:getParkInfoData>
                  <cfc:login>{config.username}</cfc:login>
                  <cfc:password>{config.password}</cfc:password>
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

      f = open(outputfile, "a", encoding='utf8')
      f.write(json.dumps(query) + "\n")
      f.close()

except (requests.exceptions.SSLError, TypeError, TimeoutError, requests.exceptions.ConnectionError) as e:
   response = None