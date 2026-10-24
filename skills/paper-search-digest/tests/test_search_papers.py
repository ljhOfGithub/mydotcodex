import importlib.util
import pathlib
import unittest
import urllib.error
from unittest import mock


SCRIPT_PATH = pathlib.Path("/Users/jackie/.codex/skills/paper-search-digest/scripts/search_papers.py")
SPEC = importlib.util.spec_from_file_location("paper_search_digest_search_papers", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class RetryRequestTests(unittest.TestCase):
    def setUp(self):
        MODULE.PROXY_DISABLED = False

    def test_retry_request_retries_transient_urlerror_until_success(self):
        attempts = {"count": 0}

        def flaky_fetch():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise urllib.error.URLError(PermissionError(1, "Operation not permitted"))
            return b"%PDF-ok"

        original_sleep = MODULE.time.sleep
        MODULE.time.sleep = lambda _seconds: None
        try:
            result = MODULE.retry_request(
                flaky_fetch,
                url="https://example.com/paper.pdf",
                timeout=30,
                label="byte request",
            )
        finally:
            MODULE.time.sleep = original_sleep

        self.assertEqual(result, b"%PDF-ok")
        self.assertEqual(attempts["count"], 3)

    def test_retry_request_stops_on_non_transient_http_error(self):
        attempts = {"count": 0}

        def bad_fetch():
            attempts["count"] += 1
            raise urllib.error.HTTPError(
                "https://example.com/missing.pdf",
                404,
                "Not Found",
                hdrs=None,
                fp=None,
            )

        with self.assertRaises(urllib.error.HTTPError):
            MODULE.retry_request(
                bad_fetch,
                url="https://example.com/missing.pdf",
                timeout=30,
                label="byte request",
            )

        self.assertEqual(attempts["count"], 1)

    def test_retry_request_has_a_bounded_attempt_count(self):
        attempts = {"count": 0}

        def always_blocked():
            attempts["count"] += 1
            raise urllib.error.URLError(PermissionError(1, "Operation not permitted"))

        original_sleep = MODULE.time.sleep
        MODULE.time.sleep = lambda _seconds: None
        try:
            with self.assertRaises(urllib.error.URLError):
                MODULE.retry_request(
                    always_blocked,
                    url="https://example.com/blocked",
                    timeout=30,
                    label="text request",
                )
        finally:
            MODULE.time.sleep = original_sleep

        self.assertEqual(attempts["count"], MODULE.MAX_RETRY_ATTEMPTS)

    def test_request_text_uses_direct_connection_after_proxy_permission_failure(self):
        attempts = {"proxy": 0, "direct": 0}

        def blocked_urlopen(_req, timeout):
            attempts["proxy"] += 1
            raise urllib.error.URLError(PermissionError(1, "Operation not permitted"))

        class DirectResponse:
            def read(self):
                attempts["direct"] += 1
                return b"{\"ok\": true}"

        class DirectOpener:
            def open(self, _req, timeout):
                return DirectResponse()

        original_sleep = MODULE.time.sleep
        MODULE.time.sleep = lambda _seconds: None
        try:
            with mock.patch.object(MODULE.urllib.request, "urlopen", side_effect=blocked_urlopen):
                with mock.patch.object(MODULE.urllib.request, "build_opener", return_value=DirectOpener()):
                    result = MODULE.request_text("https://example.com/data")
        finally:
            MODULE.time.sleep = original_sleep

        self.assertEqual(result, '{"ok": true}')
        self.assertEqual(attempts["proxy"], MODULE.MAX_RETRY_ATTEMPTS)
        self.assertEqual(attempts["direct"], 1)

    def test_proxy_stays_disabled_for_following_requests(self):
        calls = {"proxy": 0, "direct": 0}

        def blocked_urlopen(_req, timeout):
            calls["proxy"] += 1
            raise urllib.error.URLError(PermissionError(1, "Operation not permitted"))

        class DirectResponse:
            def read(self):
                calls["direct"] += 1
                return b"ok"

        class DirectOpener:
            def open(self, _req, timeout):
                return DirectResponse()

        original_sleep = MODULE.time.sleep
        MODULE.time.sleep = lambda _seconds: None
        try:
            with mock.patch.object(MODULE.urllib.request, "urlopen", side_effect=blocked_urlopen):
                with mock.patch.object(MODULE.urllib.request, "build_opener", return_value=DirectOpener()):
                    MODULE.request_text("https://example.com/first")
                    MODULE.request_text("https://example.com/second")
        finally:
            MODULE.time.sleep = original_sleep

        self.assertEqual(calls["proxy"], MODULE.MAX_RETRY_ATTEMPTS)
        self.assertEqual(calls["direct"], 2)


if __name__ == "__main__":
    unittest.main()
