import json
from unittest import mock
from unittest.mock import patch
from blueprints.main.filterresource import FilterResource
import dicttoxml

class TestMockOpeapiImageFiltering():
	sample_image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Nelumno_nucifera_open_flower_-_botanic_garden_adelaide2.jpg/800px-Nelumno_nucifera_open_flower_-_botanic_garden_adelaide2.jpg'
	sample_app_id = '56b58z0682b1dc7d81c6zd2217781d55'
	sample_key = '11f0c4d55d0fa1d1d5f175a00f0561d5'
	sample_request_id = 'c8c4ffa9-b8a0-4438-ba8d-ae3cc2cb6c46'

	def mocked_requests_get(*args, **kwargs):
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.text = dicttoxml.dicttoxml(json_data, attr_type=False, custom_root='image_process_response')
				self.status_code = status_code

			def json(self):
				return self.json_data

		if len(args) > 0:
			if args[0] == "http://opeapi.ws.pho.to/getresult":
				if kwargs['params']['request_id'] == TestMockOpeapiImageFiltering.sample_request_id:
					return MockResponse({
							'status': 'OK',
							'nowm_image_url': 'http://worker-images.ws.pho.to/i1/4CA224E3-92C8-4AFD-91A5-BE2FEB5947C0.jpg'
					}, 200)
				else:
					return MockResponse({'status': 'Error'}, 200)


		else:
			return MockResponse(None, 404)

	def mocked_requests_post(*args, **kwargs):
		
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.text = dicttoxml.dicttoxml(json_data, attr_type=False, custom_root='image_process_response')
				self.status_code = status_code

			
	
		if len(args) > 0:
			if args[0] == "http://opeapi.ws.pho.to/addtask/":
				if kwargs['data']['app_id'] == TestMockOpeapiImageFiltering.sample_app_id:
					return MockResponse({
							'status': 'OK',
							"request_id":"c8c4ffa9-b8a0-4438-ba8d-ae3cc2cb6c46"
					}, 200)
				elif kwargs['data']['app_id'] == '1':
					return MockResponse({
							'status': 'OK',
							"request_id":"123"
					}, 200)
				else:
					return MockResponse({'status': 'Error'}, 200)

		else:
			return MockResponse(None, 404)


	@mock.patch('requests.post', side_effect=mocked_requests_post)
	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_image_filtering(self, test_reqget_mock, test_reqpost_mock):

		img_filter = FilterResource()


		# Testing Function utk filter Blur pd image dengan hasil benar
		result = img_filter.proceedBlurring(self.sample_app_id, self.sample_key, self.sample_image,1)

		assert result['status'].lower() == 'successful'
		assert result['img_url'] != None

		# Testing Function utk filter Blur pd image 
		# dengan hasil error (cth: berhasil di proses request task, tapi request id invalid, sehingga 3rd Party mengembalikan response error)
		# API di http://opeapi.ws.pho.to, selalu mengembalikan status code 200 walau error
		result = img_filter.proceedBlurring('1','2', self.sample_image)
		assert result['status'].lower() != 'successful'

		# Testing Function utk filter Blur pd image 
		# dengan hasil error (cth: fail total dari proses request task, sehingga 3rd Party mengembalikan response error)
		# API di http://opeapi.ws.pho.to, selalu mengembalikan status code 200 walau error
		result = img_filter.proceedBlurring('2','2', self.sample_image)
		assert result['status'].lower() != 'successful'



		# # Testing Function utk filter Desaturate pd image dengan hasil benar
		result = img_filter.proceedDesaturate(self.sample_app_id, self.sample_key, self.sample_image)

		assert result['status'].lower() == 'successful'
		assert result['img_url'] != None

		# Testing Function utk filter Desaturate pd image 
		# dengan hasil error (cth: berhasil di proses request task, tapi request id invalid, sehingga 3rd Party mengembalikan response error)
		# API di http://opeapi.ws.pho.to, selalu mengembalikan status code 200 walau error
		result = img_filter.proceedDesaturate('1','2', self.sample_image)
		assert result['status'].lower() != 'successful'

		# Testing Function utk filter Desaturate pd image 
		# dengan hasil error (cth: fail total dari proses request task, sehingga 3rd Party mengembalikan response error)
		# API di http://opeapi.ws.pho.to, selalu mengembalikan status code 200 walau error
		result = img_filter.proceedDesaturate('2','2', self.sample_image)
		assert result['status'].lower() != 'successful'


		# Testing Function yg digunakan utk memproses request task id 
		# dari API di http://opeapi.ws.pho.to
		#dengan hasil berhasil
		result = img_filter.proceedReqId(self.sample_request_id)

		assert result['status'].lower() == 'successful'
		assert result['img_url'] != None

		# Testing Function yg digunakan utk memproses request task id 
		# dari API di http://opeapi.ws.pho.to
		#dengan hasil gagal, contoh : request id tidak valid
		result = img_filter.proceedReqId('1')
		assert result['status'].lower() != 'successful'