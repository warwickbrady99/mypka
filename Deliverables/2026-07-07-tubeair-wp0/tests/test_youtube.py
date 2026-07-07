import unittest

from tubeair.youtube import YouTubeUrlError, extract_video_id


class TestYouTubeUrlParsing(unittest.TestCase):
    def test_extract_video_id(self):
        examples = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtube.com/watch?v=dQw4w9WgXcQ&t=42s", "dQw4w9WgXcQ"),
            ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://music.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ?si=abc123", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ]

        for url, expected in examples:
            with self.subTest(url=url):
                self.assertEqual(extract_video_id(url), expected)

    def test_extract_video_id_rejects_invalid_urls(self):
        examples = [
            "https://example.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch",
            "https://youtu.be/not-valid",
            "",
        ]

        for url in examples:
            with self.subTest(url=url):
                with self.assertRaises(YouTubeUrlError):
                    extract_video_id(url)


if __name__ == "__main__":
    unittest.main()
