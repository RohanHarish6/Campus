import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from organizer import create_project, list_projects


class OrganizerTests(unittest.TestCase):
    def test_create_project_writes_categorized_timestamped_path_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp) / "projects"
            created_at = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)

            path = create_project(
                base_dir=base_dir,
                name="AI Campus Portal",
                category="Web Apps",
                description="Portal project",
                created_at=created_at,
            )

            self.assertIn("web-apps/2026-01-15/20260115T123045Z-ai-campus-portal", str(path))
            metadata = json.loads((path / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["name"], "AI Campus Portal")
            self.assertEqual(metadata["category"], "Web Apps")
            self.assertEqual(metadata["description"], "Portal project")

    def test_list_projects_returns_sorted_project_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp) / "projects"
            create_project(
                base_dir=base_dir,
                name="Later",
                category="tools",
                created_at=datetime(2026, 1, 15, 12, 30, 50, tzinfo=timezone.utc),
            )
            first = create_project(
                base_dir=base_dir,
                name="Earlier",
                category="tools",
                created_at=datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc),
            )

            projects = list(list_projects(base_dir))
            self.assertEqual(projects[0], first)


if __name__ == "__main__":
    unittest.main()
