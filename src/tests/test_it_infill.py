import os
from unittest import TestCase

from fastapi.testclient import TestClient

from main import app
from main.configuration import Context
from main.services.mistral.mistral_fim_wrapper import MistralFimWrapper


class TestInfill(TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_infill_delegates_to_service(self):
        resp = self.client.post("/infill", json={
            "input_prefix": "The quick brown fox ",
            "input_suffix": "the lazy dog ",
            "prompt": "",
        })
        self.assertIn("jumps over", resp.text.strip())

        resp = self.client.post("/infill", json={
            "input_prefix": "The quick brown fox ",
            "input_suffix": "",
            "prompt": "",
        })
        self.assertIn("jumps over the", resp.text.strip())


class TestContext(TestCase):

    def test_chooses_mistral_wrapper_when_configured(self):
        previous_provider = os.environ.get("FIM_PROVIDER")
        previous_key = os.environ.get("MISTRAL_API_KEY")
        try:
            os.environ["FIM_PROVIDER"] = "MISTRAL"
            os.environ["MISTRAL_API_KEY"] = "fake"
            wrapper = Context.get_ai_provider()
            self.assertIsInstance(wrapper, MistralFimWrapper)
        finally:
            self._restore_env("FIM_PROVIDER", previous_provider)
            self._restore_env("MISTRAL_API_KEY", previous_key)

    def _restore_env(self, key: str, value: str | None) -> None:
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
