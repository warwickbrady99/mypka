import unittest

from tubeair.transcript import select_transcript_from_api


class FakeTrack:
    def __init__(self, language_code, language, is_generated, is_translatable=False):
        self.language_code = language_code
        self.language = language
        self.is_generated = is_generated
        self.is_translatable = is_translatable
        self.translated_to = None

    def translate(self, language_code):
        translated = FakeTrack(language_code, f"Translated {language_code}", self.is_generated)
        translated.translated_to = language_code
        return translated


class TestTranscriptSelection(unittest.TestCase):
    def test_prefers_manual_preferred_language(self):
        generated_en = FakeTrack("en", "English", True)
        manual_en = FakeTrack("en", "English", False)

        selected, translated = select_transcript_from_api([generated_en, manual_en], preferred_language="en")

        self.assertEqual(selected, manual_en)
        self.assertFalse(translated)

    def test_uses_generated_preferred_language_when_manual_missing(self):
        generated_en = FakeTrack("en", "English", True)
        manual_de = FakeTrack("de", "German", False)

        selected, translated = select_transcript_from_api([manual_de, generated_en], preferred_language="en")

        self.assertEqual(selected, generated_en)
        self.assertFalse(translated)

    def test_allows_translation_when_requested(self):
        manual_de = FakeTrack("de", "German", False, is_translatable=True)

        selected, translated = select_transcript_from_api([manual_de], preferred_language="en", allow_translation=True)

        self.assertEqual(selected.language_code, "en")
        self.assertTrue(translated)

    def test_falls_back_to_best_original_language(self):
        generated_de = FakeTrack("de", "German", True)
        manual_fr = FakeTrack("fr", "French", False)

        selected, translated = select_transcript_from_api([generated_de, manual_fr], preferred_language="en")

        self.assertEqual(selected, manual_fr)
        self.assertFalse(translated)


if __name__ == "__main__":
    unittest.main()
