import unittest
import json
import pandas as pd
from werkzeug.datastructures import FileStorage

from flask_app_test import app
from flask_app_test.models import UserModel, UserDataModel, UserDataDetailModel

USERNAME = 'johnsmith'
PASSWORD = 'Welcome123$'
FILE_NAME = 'sample-dataset-small.xlsm'
# FILE_NAME = 'sample-dataset.xlsm'
FILE_PATH = 'DATA\\' + FILE_NAME

def login(client):
    payload = json.dumps({
        'username': USERNAME,
        'password': PASSWORD
    })
    return client.post('/api/dm/login', headers={'Content-Type': 'application/json'}, data=payload)

def post_datafile(client, token):
    headers = None
    if token:
        headers={'Authorization': 'Bearer %s' % token}
    
    file_name = FILE_NAME
    form_data = {
        'file': FileStorage(stream=open(FILE_PATH, 'rb'), filename=file_name)
    }

    return client.post('/api/dm/datafiles', headers=headers, content_type='multipart/form-data', data=form_data)

def get_datafiles(client, token):
    headers = None
    if token:
        headers={'Authorization': 'Bearer %s' % token}

    return client.get('/api/dm/datafiles?offset=0&limit=100', headers=headers)

def get_datafiledetails(client, token, id):
    headers = None
    if token:
        headers={'Authorization': 'Bearer %s' % token}

    return client.get('/api/dm/datafiles/%d?offset=0&limit=100' % id, headers=headers)

class LoginTest(unittest.TestCase):
    """
    Tests for user login.
    """
    def setUp(self):
        self.client = app.test_client()

    def test_login(self):
        """
        Ensure user can login and get access token.
        """
        response = login(self.client)
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, type(response.json['access_token']))

class DataFileTest(unittest.TestCase):
    """
    Tests for user dataset management.
    """
    def setUp(self):
        self.client = app.test_client()
        
        login_response = login(self.client)
        self.token = login_response.json['access_token']

        user = UserModel.find_by_user_name(USERNAME)
        self.user_id = user.id

    def test_datafile_post(self):
        """
        Ensure user can create new dataset.
        """
        post_datafile_response = post_datafile(self.client, self.token)
        self.assertEqual(201, post_datafile_response.status_code)

        datafile_id = post_datafile_response.json['id']
        datafile = UserDataModel.query.filter_by(id=datafile_id).first()
        self.assertEqual(FILE_NAME, datafile.data_file_name)

        df = pd.read_excel(FILE_PATH)
        df_valid = df[pd.to_numeric(df['Value'], errors='coerce').notnull()]
        df_invalid = df[pd.to_numeric(df['Value'], errors='coerce').isnull()]
        self.assertEqual(len(df), datafile.total_count)
        self.assertEqual(len(df_valid), datafile.success_count)
        self.assertEqual(len(df_invalid), datafile.fail_count)

        datafiledetails = UserDataDetailModel.query.filter_by(user_data_id=datafile_id).order_by(UserDataDetailModel.id.asc())
        for (i, row), datafiledetail in zip(df_valid.iterrows(), datafiledetails):
            self.assertEqual(datafiledetail.data_year, row['Year'])
            self.assertEqual(datafiledetail.industry_aggregation_nzsioc, row['Industry_aggregation_NZSIOC'])
            self.assertEqual(datafiledetail.industry_code_nzsioc, str(row['Industry_code_NZSIOC']))
            self.assertEqual(datafiledetail.industry_name_nzsioc, row['Industry_name_NZSIOC'])
            self.assertEqual(datafiledetail.units, row['Units'])
            self.assertEqual(datafiledetail.variable_code, row['Variable_code'])
            self.assertEqual(datafiledetail.variable_name, row['Variable_name'])
            self.assertEqual(datafiledetail.variable_category, row['Variable_category'])
            self.assertEqual(datafiledetail.data_value, row['Value'])

    def test_datafile_get(self):
        """
        Ensure user can list dataset.
        """
        get_datafiles_response = get_datafiles(self.client, self.token)
        self.assertEqual(200, get_datafiles_response.status_code)
        
        count = UserDataModel.query.filter_by(user_id=self.user_id).count()
        self.assertEqual(count, get_datafiles_response.json['count'])

        datafiles = UserDataModel.query.filter_by(user_id=self.user_id)
        result = get_datafiles_response.json['result']
        for datafile in datafiles:
            for r in result:
                if datafile.id == r['id']:
                    self.assertEqual(datafile.data_file_name, r['data_file_name'])
                    self.assertEqual(datafile.total_count, r['total_count'])
                    self.assertEqual(datafile.success_count, r['success_count'])
                    self.assertEqual(datafile.fail_count, r['fail_count'])
                    self.assertEqual(datafile.created_time.strftime('%Y-%m-%d %H:%M:%S'), r['created_time'])

    def test_datafile_post_unauthorized(self):
        """
        Ensure anonymous user cannot create any dataset.
        """
        post_datafile_response = post_datafile(self.client, '')
        self.assertEqual(401, post_datafile_response.status_code)

    def test_datafile_get_unauthorized(self):
        """
        Ensure anonymous user cannot list any dataset.
        """
        get_datafiles_response = get_datafiles(self.client, '')
        self.assertEqual(401, get_datafiles_response.status_code)

class DataFileDetailTest(unittest.TestCase):
    """
    Tests for user dataset details.
    """
    def setUp(self):
        self.client = app.test_client()
        
        login_response = login(self.client)
        self.token = login_response.json['access_token']
        
        post_datafile_response = post_datafile(self.client, self.token)
        self.datafile_id = post_datafile_response.json['id']

    def test_datafiledetails_get(self):
        """
        Ensure user can view dataset details.
        """
        get_datafiledetails_response = get_datafiledetails(self.client, self.token, self.datafile_id)
        self.assertEqual(200, get_datafiledetails_response.status_code)

        count = UserDataDetailModel.query.filter_by(user_data_id=self.datafile_id).count()
        self.assertEqual(count, get_datafiledetails_response.json['count'])

        datafiledetails = UserDataDetailModel.query.filter_by(user_data_id=self.datafile_id).order_by(UserDataDetailModel.id.asc()).limit(100)
        result = get_datafiledetails_response.json['result']
        for datafiledetail, r in zip(datafiledetails, result):
            self.assertEqual(datafiledetail.data_year, r['data_year'])
            self.assertEqual(datafiledetail.industry_aggregation_nzsioc, r['industry_aggregation_nzsioc'])
            self.assertEqual(datafiledetail.industry_code_nzsioc, r['industry_code_nzsioc'])
            self.assertEqual(datafiledetail.industry_name_nzsioc, r['industry_name_nzsioc'])
            self.assertEqual(datafiledetail.units, r['units'])
            self.assertEqual(datafiledetail.variable_code, r['variable_code'])
            self.assertEqual(datafiledetail.variable_name, r['variable_name'])
            self.assertEqual(datafiledetail.variable_category, r['variable_category'])
            self.assertEqual(datafiledetail.data_value, r['data_value'])

    def test_datafiledetails_get_unauthorized(self):
        """
        Ensure anonymous user cannot view dataset details.
        """
        get_datafiledetails_response = get_datafiledetails(self.client, '', self.datafile_id)
        self.assertEqual(401, get_datafiledetails_response.status_code)

if __name__ == '__main__':
    unittest.main()
