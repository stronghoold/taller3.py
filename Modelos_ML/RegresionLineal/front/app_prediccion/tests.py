import os
from unittest import mock

from django.test import Client, TestCase


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_renders_form(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tasador de Viviendas", response.content.decode())

    @mock.patch.dict(os.environ, {"API_URL": "http://api.test/predict"})
    @mock.patch("app_prediccion.views.requests.post")
    def test_post_shows_formatted_prediction(self, post):
        post.return_value.status_code = 200
        post.return_value.json.return_value = {"predicted_price": 189802.33}

        response = self.client.post("/", {"area_m2": "85.5"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("189,802.33", response.content.decode())

    def test_post_rejects_non_numeric_area(self):
        response = self.client.post("/", {"area_m2": "abc"})
        self.assertIn("85.5", response.content.decode())

    def test_post_rejects_empty_area(self):
        response = self.client.post("/", {"area_m2": ""})
        self.assertIn("Debes ingresar", response.content.decode())

    @mock.patch("app_prediccion.views.requests.post")
    def test_post_reports_api_error_status(self, post):
        post.return_value.status_code = 503

        response = self.client.post("/", {"area_m2": "85.5"})

        self.assertIn("código 503", response.content.decode())

    @mock.patch("app_prediccion.views.requests.post")
    def test_post_reports_connection_failure(self, post):
        import requests

        post.side_effect = requests.exceptions.ConnectionError

        response = self.client.post("/", {"area_m2": "85.5"})

        self.assertIn("No se pudo conectar", response.content.decode())
