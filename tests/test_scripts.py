"""Tests for the checker scripts and the build. Run: python -m unittest discover -s tests -v"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script: str, text: str, *args: str, code: int = 0) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        path = f.name
    out = subprocess.run([sys.executable, str(ROOT / script), path, *args], capture_output=True, text=True)
    assert out.returncode == code, f"exit {out.returncode} != {code}\n{out.stdout}{out.stderr}"
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

    def test_help_and_non_achievement_sections(self):
        out = subprocess.run([sys.executable, str(ROOT / self.script), "--help"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0)
        cv = ("## EDUCATION\n- Relevant coursework: Data Structures, Statistics\n- Cumulative GPA: 3.68 / 4.00\n"
              "## PROJECTS\n- Built a quiz game used by 15 classmates\n- Wrote an 84-run evaluation harness\n"
              "## SKILLS\n- Python, C++, SQL\n")
        out = run(self.script, cv, "--strict")
        self.assertIn("2/2", out)

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


    def test_ieee_ranges_and_code_are_not_errors(self):
        text = "Prior work [1], [2]-[4] and [5-6] shows this. Code: arr[7] = x[0] and `y[9]`.\n\n## References\n[1] a\n[2] b\n[3] c\n[4] d\n[5] e\n[6] f\n"
        out = run(self.script, text)
        self.assertIn("Result: OK", out)

    def test_apa_hard_cases(self):
        text = ("Health matters (World Health Organization, 2020). See van Dijk (2019), (Santoso, Lee, & Park, 2021), "
                "(Darwin, 1859) and (lihat Hadi, 2017, hlm. 4). Menurut Kurniawan dan Sari (2018), ini benar.\n\n# References\n\n"
                "World Health Organization. (2020). Report.\nvan Dijk, T. (2019). Text.\nSantoso, B., Lee, J., & Park, S. (2021). Paper.\n"
                "Darwin, C. (1859). Origin.\nHadi, R. (2017). E.\nKurniawan, A., & Sari, D. (2018). D.\n")
        out = run(self.script, text)
        self.assertIn("Result: OK", out)

    def test_strict_exit_code(self):
        run(self.script, "See [1].\n\n## References\n[1] a\n[2] b\n", "--strict", code=1)
        run(self.script, "See [1].\n\n## References\n[1] a\n", "--strict", code=0)


class TextCheck(unittest.TestCase):
    script = "shared/scripts/text_check.py"

    def test_indonesian_padding_and_signifikan(self):
        text = ("Di era digital yang semakin berkembang, teknologi memainkan peran penting. Tidak dapat dipungkiri bahwa data itu penting.\n\n"
                "Selain itu, hasilnya signifikan [DATA NEEDED: angka].\n\nSelain itu, ini juga berguna.")
        out = run(self.script, text, "--lang", "id")
        for expected in ('"di era digital"', "tidak dapat dipungkiri", "memainkan peran penting",
                         "selain itu", "without a test result in the same sentence", "DATA NEEDED"):
            self.assertIn(expected, out)

    def test_signifikan_with_test_is_fine(self):
        out = run(self.script, "Hasilnya signifikan (t(28) = 2,41; p = 0,02) dan konsisten dengan studi sebelumnya.", "--lang", "id")
        self.assertNotIn("without a test result", out)

    def test_test_result_in_another_paragraph_does_not_count(self):
        out = run(self.script, "Proyek saya signifikan.\n\nUji t menunjukkan p = 0,02.", "--lang", "id")
        self.assertIn("without a test result in the same sentence", out)


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

    def test_significance_needs_test_in_sentence(self):
        out = run(self.script, "Hasilnya signifikan. Perbedaannya signifikan (uji t, p = 0,03).", "--per-sentence")
        flagged = [l for l in out.splitlines() if l.startswith("!")]
        self.assertEqual(len(flagged), 1, out)
        self.assertIn("Hasilnya signifikan", flagged[0])

    def test_compare(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d, "a.txt"), Path(d, "b.txt")
            a.write_text("Furthermore, this pivotal journey was a testament to my passion. Furthermore, it is crucial.", encoding="utf-8")
            b.write_text("I kept fixing the same bug for a week. Then it worked.", encoding="utf-8")
            out = subprocess.run([sys.executable, str(ROOT / self.script), "--compare", str(a), str(b)],
                                 capture_output=True, text=True, check=True).stdout
        self.assertIn("Total flags", out)
        self.assertRegex(out, r"Total flags\s+\d+\s+0")


class Strict(unittest.TestCase):
    def test_ps_and_humanize_strict(self):
        bad = "This journey was a testament to my passion. In conclusion, I promise to work hard."
        run("skills/personal-statement/scripts/ps_check.py", bad, "--strict", code=1)
        run("skills/humanizer/scripts/humanize_check.py", bad, "--strict", code=1)
        run("shared/scripts/text_check.py", "Di era digital, tidak dapat dipungkiri, teknologi memainkan peran penting.", "--lang", "id", "--strict", code=1)


class ReviewTwoRegressions(unittest.TestCase):
    """Cases found by the second independent review (v2.0.2)."""

    def test_first_person_counts_as_voice(self):
        out = run("skills/humanizer/scripts/humanize_check.py",
                  "We tested the new design on the team for a week. My mother taught me to cook before school.",
                  "--per-sentence")
        self.assertIn("Sentences with flags: 0/2", out)

    def test_technical_terms_are_not_heavy(self):
        out = run("skills/humanizer/scripts/humanize_check.py",
                  "We used robust standard errors and a wiring harness. CPU utilization dropped from 80% to 45%. "
                  "The robust navigation stack ran in landscape mode during the landscape survey.")
        self.assertIn("light touch", out)

    def test_repo_markers_are_placeholders_but_math_is_not(self):
        out = run("skills/personal-statement/scripts/ps_check.py", "I built it [ADD DETAIL: which?] and [DATA NEEDED: accuracy].")
        self.assertIn("[ADD DETAIL: which?]", out)
        self.assertIn("[DATA NEEDED: accuracy]", out)
        out = run("skills/personal-statement/scripts/ps_check.py", "x < 3 and y > 9, see <https://example.com> and <div>.")
        self.assertIn("Result: OK", out)
        out = run("skills/personal-statement/scripts/ps_check.py", "My example: <write_your_example_here>.")
        self.assertIn("<write_your_example_here>", out)

    def test_cite_more_apa_forms(self):
        text = ("As Santoso, Lee, and Park (2021) and Santoso's (2023) work shows (WHO, 2020), see Lee (2021) and Smith (2020).\n\n"
                "# References\n\nSantoso, B., Lee, J., & Park, S. (2021). P.\nSantoso, B. (2023). Q.\n"
                "World Health Organization [WHO]. (2020). R.\nLee, J. (2021, March 5). Blog post.\nSmith, J. 2020. Judul Buku. Penerbit.\n")
        self.assertIn("Result: OK", run("shared/scripts/cite_check.py", text))

    def test_cite_gbt_intervals_and_years(self):
        text = ("张三[1]指出，李四[2]-[3]。数组 arr[7] 和区间 [0, 255]、[2010-2020]。\n\n参考文献\n"
                "[1] 张三. 标题[J]. 2020.\n[2] 李四. 标题[M]. 2019.\n[3] 王五. 标题[D]. 2021.\n")
        self.assertIn("Result: OK", run("shared/scripts/cite_check.py", text))

    def test_cite_huge_range_is_fast(self):
        import time
        start = time.time()
        run("shared/scripts/cite_check.py", "See [1] and [1-300000].\n\n## References\n[1] a\n")
        self.assertLess(time.time() - start, 5)

    def test_cite_empty_list_and_utf16(self):
        out = run("shared/scripts/cite_check.py", "Text [1].\n\n## References\n")
        self.assertIn("list under it is empty", out)
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-16") as f:
            f.write("See [1].\n\n## References\n[1] a\n")
        out = subprocess.run([sys.executable, str(ROOT / "shared/scripts/cite_check.py"), f.name],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("Result: OK", out)

    def test_strict_in_per_sentence_and_compare(self):
        run("skills/humanizer/scripts/humanize_check.py", "Next, she explains the science behind carbon in detail.",
            "--per-sentence", "--strict", code=1)
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d, "a.txt"), Path(d, "b.txt")
            a.write_text("This journey was a testament to my passion.", encoding="utf-8")
            b.write_text("It was a testament to my delving.", encoding="utf-8")
            out = subprocess.run([sys.executable, str(ROOT / "skills/humanizer/scripts/humanize_check.py"),
                                  "--compare", str(a), str(b), "--strict"], capture_output=True, text=True)
            self.assertEqual(out.returncode, 1, out.stdout)

    def test_empty_input_warns(self):
        for script in ("skills/personal-statement/scripts/ps_check.py", "skills/humanizer/scripts/humanize_check.py",
                       "shared/scripts/text_check.py", "skills/harvard-cv/scripts/cv_check.py"):
            out = run(script, "   \n")
            self.assertIn("Empty input", out, script)


class ReviewThreeRegressions(unittest.TestCase):
    """Cases found by the third independent review (v2.0.3)."""

    def test_landscape_is_detectable(self):
        out = run("skills/humanizer/scripts/humanize_check.py", "The evolving landscape of AI is changing everything for us.")
        self.assertIn("landscape", out)

    def test_ps_check_indonesian(self):
        out = run("skills/personal-statement/scripts/ps_check.py",
                  "Di era digital yang semakin berkembang, teknologi memainkan peran penting. "
                  "Tidak dapat dipungkiri bahwa data merupakan hal yang sangat penting bagi saya.")
        self.assertIn("Language: id", out)
        self.assertIn("di era digital", out)
        self.assertNotIn("Result: OK", out)

    def test_passive_methods_not_flagged(self):
        out = run("skills/humanizer/scripts/humanize_check.py",
                  "The solution was heated for ten minutes. The sample was weighed on a balance. The mixture was stirred until clear.",
                  "--per-sentence")
        self.assertIn("Sentences with flags: 0/3", out)

    def test_register_report_skips_anchor(self):
        out = run("skills/humanizer/scripts/humanize_check.py",
                  "This section describes the overall approach used throughout the whole project.", "--per-sentence",
                  "--register", "report")
        self.assertNotIn("no concrete anchor", out)

    def test_first_person_not_fooled_by_bab_i_or_us(self):
        out = run("skills/humanizer/scripts/humanize_check.py",
                  "Bab I membahas latar belakang secara umum dan menyeluruh sekali.", "--per-sentence", "--lang", "id")
        self.assertIn("no concrete anchor", out)

    def test_triplet_and_abbreviations(self):
        out = run("skills/humanizer/scripts/humanize_check.py",
                  "Yesterday, I went and bought bread. The U.S. data from Dr. Lee, e.g. the 2020 survey, was clear.")
        self.assertNotIn("Lists of three", out)
        self.assertIn("Sentences: 2", out)

    def test_crlf_character_count(self):
        a = run("skills/personal-statement/scripts/ps_check.py", "One line.\nTwo line.\n")
        b = run("skills/personal-statement/scripts/ps_check.py", "One line.\r\nTwo line.\r\n")
        grab = lambda s: [l for l in s.splitlines() if l.startswith("Characters (with spaces)")][0]
        self.assertEqual(grab(a), grab(b))

    def test_utf16_without_bom(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".txt", delete=False) as f:
            f.write("My project was a testament to my passion.".encode("utf-16-le"))
        out = subprocess.run([sys.executable, str(ROOT / "skills/personal-statement/scripts/ps_check.py"), f.name],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("testament", out)

    def test_compare_with_empty_after(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d, "a.txt"), Path(d, "b.txt")
            a.write_text("This journey was a testament to my passion.", encoding="utf-8")
            b.write_text("", encoding="utf-8")
            out = subprocess.run([sys.executable, str(ROOT / "skills/humanizer/scripts/humanize_check.py"),
                                  "--compare", str(a), str(b), "--strict"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertIn("Empty input", out.stdout)

    def test_cite_apa_appendix_multiyear_abbr_heading(self):
        text = ("Data were collected (Hadi, 2017). In Indonesia (2020) the rules changed. Santoso was (born 2001) here "
                "(Santoso, 2020, 2021). Health (World Health Organization [WHO], 2020); later (WHO, 2020).\n\n"
                "# Reference List\n\nHadi, R. (2017). E.\nSantoso, B. (2020). A.\nSantoso, B. (2021). B.\n"
                "World Health Organization. (2020). R.\n\n# Lampiran\n\nData collected in (2019) survey.\n")
        out = run("shared/scripts/cite_check.py", text)
        self.assertIn("Result: OK", out)
        self.assertIn("? Possible citation", out)
        self.assertNotIn("Data Collected", out)

    def test_cite_footnotes_and_works_cited(self):
        out = run("shared/scripts/cite_check.py", "A claim.[^1]\n\n[^1]: Smith, Book (2020).\n\n## Works Cited\n\nSmith, J. (2020). Book.\n")
        self.assertIn("Footnote", out)


class Build(unittest.TestCase):
    def test_every_skill_front_matter_is_valid_yaml(self):
        import re
        import yaml
        for skill_md in (ROOT / "skills").glob("*/SKILL.md"):
            m = re.match(r"^---\s*\n(.*?)\n---", skill_md.read_text(encoding="utf-8"), re.S)
            self.assertIsNotNone(m, skill_md)
            fm = yaml.safe_load(m.group(1))
            self.assertEqual(fm["name"], skill_md.parent.name)
            self.assertLessEqual(len(fm["description"]), 1024, skill_md)

    def test_marketplace_name_is_fixed(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("build", ROOT / "scripts" / "build.py")
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        self.assertEqual(build.repo_info()["owner"], "Vetame21")

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
