"""Tests for the checker scripts and the build. Run: python -m unittest discover -s tests -v"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script: str, text: str, *args: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    out = subprocess.run([sys.executable, str(ROOT / script), path, *args],
                         capture_output=True, text=True, check=True)
    return out.stdout


class PersonalStatementCheck(unittest.TestCase):
    script = "skills/personal-statement/scripts/ps_check.py"

    def test_flags_ai_phrases_and_placeholders(self):
        out = run(self.script, "This journey was a testament to my passion. It is not just about code, but about people. "
                               "In conclusion, I promise to work hard <write_your_example_here>.", "--limit-words", "10")
        for expected in ("testament", "journey", "in conclusion", "i promise", "Over word limit", "<write_your_example_here>"):
            self.assertIn(expected, out)

    def test_clean_text_passes(self):
        out = run(self.script, "I built a quiz game. It broke often. Fixing it taught me to test one step at a time.")
        self.assertIn("Result: OK", out)


class CvCheck(unittest.TestCase):
    script = "skills/harvard-cv/scripts/cv_check.py"

    def test_pronoun_rule(self):
        out = run(self.script, "- I built a thing\n- Studied Calculus I and II with 3 projects\n- Helped my team\n- Used US data in 2 reports\n")
        self.assertIn("line 1: personal pronoun", out)
        self.assertNotIn("line 2: personal pronoun", out)
        self.assertIn("line 3: weak opener, personal pronoun", out)
        self.assertNotIn("line 4", out)

    def test_buzzwords_and_dates(self):
        out = run(self.script, "- Successfully leveraged synergies\nSep 2024 – June 2025\n")
        self.assertIn("buzzword 'successfully'", out)
        self.assertIn("Mixed date formats", out)


class CiteCheck(unittest.TestCase):
    script = "shared/scripts/cite_check.py"

    def test_apa(self):
        text = ("Fraud rose (Santoso, 2023; Lee & Park, 2021). Wijaya et al. (2022) agree (Chen, 2020).\n\n"
                "# Daftar Pustaka\n\nLee, J., & Park, S. (2021). A.\nSantoso, B. (2023). B.\nKurniawan, A. (2019). C.\n")
        out = run(self.script, text)
        self.assertIn("Cited but not in references: Chen (2020)", out)
        self.assertIn("Cited but not in references: Wijaya (2022)", out)
        self.assertIn("In references but never cited: Kurniawan (2019)", out)

    def test_ieee(self):
        text = "See [2], [1], [3]-[4] and [6].\n\n## References\n[1] a\n[2] b\n[3] c\n[4] d\n[5] e\n"
        out = run(self.script, text)
        self.assertIn("Cited but not in references: [6]", out)
        self.assertIn("In references but never cited: [5]", out)
        self.assertIn("not in numeric order", out)


class TextCheck(unittest.TestCase):
    script = "shared/scripts/text_check.py"

    def test_indonesian_padding_and_signifikan(self):
        text = ("Di era digital yang semakin berkembang, teknologi memainkan peran penting. Tidak dapat dipungkiri bahwa data itu penting.\n\n"
                "Selain itu, hasilnya signifikan [DATA NEEDED: angka].\n\nSelain itu, ini juga berguna.")
        out = run(self.script, text, "--lang", "id")
        for expected in ('"di era digital"', "tidak dapat dipungkiri", "memainkan peran penting",
                         "selain itu", "without a nearby test result", "DATA NEEDED"):
            self.assertIn(expected, out)

    def test_signifikan_with_test_is_fine(self):
        out = run(self.script, "Hasilnya signifikan (t(28) = 2,41; p = 0,02) dan konsisten dengan studi sebelumnya.", "--lang", "id")
        self.assertNotIn("without a nearby test result", out)


class HumanizeCheck(unittest.TestCase):
    script = "skills/humanizer/scripts/humanize_check.py"

    def test_heavy_english(self):
        text = ("In today's rapidly evolving digital landscape, data science plays a pivotal role. My journey has been a testament to my passion.\n\n"
                "Furthermore, I am curious, driven, and resilient. This taught me the importance of perseverance.\n\n"
                "Furthermore, CityU offers a unique blend of rigor, community, and opportunity. It taught me that I can grow.")
        out = run(self.script, text)
        self.assertIn("heavy", out)
        self.assertIn("furthermore", out)

    def test_per_sentence_summary(self):
        text = ("Shaping Zero is a 25-minute film by Rachel Skinner, President of the Institution of Civil Engineers. "
                "Skinner narrates the film, and engineers and industry leaders also contribute. "
                "Scientists have warned for decades that human activity is overloading natural systems. "
                "Next, she explains the science behind carbon. "
                "Carbon dioxide is only about 0.04% of the atmosphere, but its concentration has gone up since the Industrial Revolution.")
        out = run(self.script, text, "--per-sentence")
        flagged = [line for line in out.splitlines() if line.startswith("!")]
        self.assertEqual(len(flagged), 2, out)
        self.assertTrue(any("Next, she explains" in l for l in flagged))
        self.assertTrue(any("Scientists have warned" in l for l in flagged))

    def test_compare(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d, "a.txt"), Path(d, "b.txt")
            a.write_text("Furthermore, this pivotal journey was a testament to my passion. Furthermore, it is crucial.", encoding="utf-8")
            b.write_text("I kept fixing the same bug for a week. Then it worked.", encoding="utf-8")
            out = subprocess.run([sys.executable, str(ROOT / self.script), "--compare", str(a), str(b)],
                                 capture_output=True, text=True, check=True).stdout
        self.assertIn("Total flags", out)
        self.assertRegex(out, r"Total flags\s+\d+\s+0")


class Build(unittest.TestCase):
    def test_build_is_up_to_date(self):
        out = subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py"), "--check"],
                             capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)

    def test_shared_copies_match(self):
        for skill in (ROOT / "skills").iterdir():
            for f in (ROOT / "shared" / "references").glob("*.md"):
                copy = skill / "references" / "shared" / f.name
                self.assertTrue(copy.exists(), copy)
                self.assertEqual(copy.read_text(encoding="utf-8"), f.read_text(encoding="utf-8"), copy)


if __name__ == "__main__":
    unittest.main()
