"""
Unit tests for process_dataset.atomic_write_json — the swap mechanism used by
the upload endpoint to overwrite card_analysis_data.json safely.

If a future refactor drops the fsync, replaces os.replace with shutil.move, or
removes the .tmp cleanup branch, these tests will fail before that change
ships. Companion to test_pipeline.py (which tests the *content* of the JSON).

Run directly:
    python tests/test_atomic_write.py

Via unittest:
    python -m unittest tests.test_atomic_write -v

Via pytest (no plugin required):
    pytest tests/test_atomic_write.py -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from process_dataset import atomic_write_json  # noqa: E402


class AtomicWriteTests(unittest.TestCase):
    """
    Verify atomic_write_json's swap mechanics:
      - happy path produces the new content
      - overwrite replaces existing content
      - no *.tmp files leak into the target dir
      - parent dirs get created if missing
      - error during write cleans up the .tmp file
    """

    def setUp(self):
        # Per-test isolated tempdir auto-cleaned on tearDown. Reused across
        # tests so MultiTest-style runs don't collide.
        self._td = tempfile.TemporaryDirectory()
        self.tmp_dir = Path(self._td.name)

    def tearDown(self):
        self._td.cleanup()

    # ------------------------------------------------------------------ #
    # happy-path: file lands with correct content                        #
    # ------------------------------------------------------------------ #

    def test_target_file_exists_with_written_content(self):
        target = self.tmp_dir / "result.json"
        payload = {"ok": True, "marker": "happy", "nested": [1, 2, 3]}

        atomic_write_json(target, payload)

        self.assertTrue(
            target.exists(),
            msg=f"target file missing after atomic_write_json: {target}",
        )
        loaded = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(
            loaded,
            payload,
            msg="read-back content differs from the payload that was passed in",
        )

    def test_overwrites_existing_target_with_new_content(self):
        target = self.tmp_dir / "result.json"
        # Pre-populate the target so we can confirm the swap replaces it
        # entirely (not: fail, or: leave stale bytes behind).
        target.write_text(json.dumps({"legacy": "data"}), encoding="utf-8")

        new_payload = {"ok": True, "marker": "replaced"}
        atomic_write_json(target, new_payload)

        loaded = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(loaded, new_payload)
        self.assertNotIn(
            "legacy",
            loaded,
            msg="old content survived the atomic swap — the swap is non-destructive",
        )

    def test_no_tmp_files_leak_into_target_directory(self):
        target = self.tmp_dir / "result.json"
        atomic_write_json(target, {"ok": True})

        leaked = sorted(p.name for p in self.tmp_dir.iterdir() if p.name.endswith(".tmp"))
        self.assertEqual(
            leaked,
            [],
            msg=(
                f"Expected zero .tmp files after a successful atomic write, "
                f"but found: {leaked}"
            ),
        )

    def test_creates_missing_parent_directories(self):
        # Nested target whose parent dir chain does not exist yet.
        target = self.tmp_dir / "deep" / "nested" / "dir" / "result.json"
        self.assertFalse(
            target.parent.exists(),
            msg="precondition failed — parent dirs already exist before the test",
        )

        atomic_write_json(target, {"ok": True, "marker": "nested"})

        self.assertTrue(target.exists(), msg="target file should exist after write")
        self.assertTrue(
            target.parent.exists(),
            msg="parent dir chain should be created by atomic_write_json",
        )

    # ------------------------------------------------------------------ #
    # error-path: .tmp gets cleaned up if the writer throws               #
    # ------------------------------------------------------------------ #

    def test_failure_during_write_leaves_no_tmp_leftover(self):
        """
        A non-JSON-serialisable payload (a `set`) makes json.dump raise
        TypeError after the .tmp was created. atomic_write_json's except
        branch should unlink the .tmp file before re-raising.
        """
        target = self.tmp_dir / "result.json"
        non_serialisable = {"this_is_a_set": {1, 2, 3}}

        with self.assertRaises(
            TypeError,
            msg="non-serialisable payload should trigger TypeError inside atomic_write_json",
        ):
            atomic_write_json(target, non_serialisable)

        leaked = sorted(p.name for p in self.tmp_dir.iterdir() if p.name.endswith(".tmp"))
        self.assertEqual(
            leaked,
            [],
            msg=(
                f"Expected zero .tmp files after an error path, "
                f"but found leftovers: {leaked}. atomic_write_json's except "
                f"branch failed to unlink the temp file before re-raising."
            ),
        )
        # And no partial target should have been created.
        self.assertFalse(
            target.exists(),
            msg="target file should NOT exist after a failed write — the swap never happened",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
