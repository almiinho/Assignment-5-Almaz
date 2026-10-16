import tempfile, unittest
from pathlib import Path
from plant_research.audit import audit_dataset, discover_images

class AuditTests(unittest.TestCase):
    def make_file(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"placeholder")
    def test_counts_by_split_and_class(self):
        with tempfile.TemporaryDirectory() as temp:
            r=Path(temp); self.make_file(r/"train"/"healthy"/"a.jpg")
            self.make_file(r/"train"/"rust"/"b.png"); self.make_file(r/"test"/"healthy"/"c.jpeg")
            report=audit_dataset(r)
            self.assertEqual(report["image_count"],3)
            self.assertEqual(report["splits"]["train"]["classes"]["healthy"],1)
            self.assertEqual(report["splits"]["test"]["total"],1)
    def test_repeated_filename_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            r=Path(temp); self.make_file(r/"train"/"healthy"/"leaf.jpg")
            self.make_file(r/"test"/"rust"/"leaf.jpg")
            self.assertEqual(audit_dataset(r)["repeated_filenames"],["leaf.jpg"])
    def test_empty_dataset_raises(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError): audit_dataset(Path(temp))
    def test_extension_case_insensitive(self):
        with tempfile.TemporaryDirectory() as temp:
            r=Path(temp); self.make_file(r/"class_a"/"leaf.JPG"); self.make_file(r/"class_a"/"note.txt")
            self.assertEqual(len(discover_images(r)),1)

if __name__ == "__main__": unittest.main()
