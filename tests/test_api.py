"""HTTP API smoke tests."""

import unittest

from fastapi.testclient import TestClient

from src.api.routes import app


class ApiSchemaTests(unittest.TestCase):
    def test_chat_request_schema_rejects_empty_message(self) -> None:
        from src.api.schemas import ChatRequest
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            ChatRequest(message="")

    def test_health_route(self) -> None:
        response = TestClient(app).get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_chat_route_rejects_empty_message(self) -> None:
        response = TestClient(app).post("/chat", json={"message": ""})

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
