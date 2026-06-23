from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_repo  # noqa: E402
from test_validate_repo import make_valid_repo, read_csv_rows, rewrite_csv, valid_profile, write_text  # noqa: E402


def errors(root: Path) -> list[str]:
    return [issue.message for issue in validate_repo.run_checks(root) if issue.level == "ERROR"]


class ProtocolTableTests(unittest.TestCase):
    def assert_has_error(self, root: Path, fragment: str) -> None:
        messages = errors(root)
        self.assertTrue(any(fragment in message for message in messages), messages)

    def test_header_overlap_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/header_fields.csv")
            rows[1]["offset_bytes"] = "3"
            rewrite_csv(root, "specs/common/protocol/header_fields.csv", rows)
            self.assert_has_error(root, "field overlap")

    def test_header_gap_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/header_fields.csv")
            rows[1]["offset_bytes"] = "5"
            rewrite_csv(root, "specs/common/protocol/header_fields.csv", rows)
            self.assert_has_error(root, "field gap")

    def test_header_total_length_not_48_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/header_fields.csv")
            rows[-1]["length_bytes"] = "3"
            rewrite_csv(root, "specs/common/protocol/header_fields.csv", rows)
            self.assert_has_error(root, "total length 47 != 48")

    def test_data_block_total_length_not_10_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/data_block_fields.csv")
            rows[-1]["length_bytes"] = "3"
            rewrite_csv(root, "specs/common/protocol/data_block_fields.csv", rows)
            self.assert_has_error(root, "total length 9 != 10")

    def test_packet_ack_pair_missing_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/packet_types.csv")
            rows[0]["ack_type_value"] = ""
            rewrite_csv(root, "specs/common/protocol/packet_types.csv", rows)
            self.assert_has_error(root, "missing ACK pair")

    def test_session_ack_pair_mismatch_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            rows = read_csv_rows(root, "specs/common/protocol/session_controls.csv")
            rows[0]["ack_detail_value"] = "99"
            rewrite_csv(root, "specs/common/protocol/session_controls.csv", rows)
            self.assert_has_error(root, "ACK target missing")

    def test_unsafe_profile_flag_true_fails(self) -> None:
        with make_valid_repo() as root_name:
            root = Path(root_name)
            profile = valid_profile()
            profile["allow_non_loopback"] = True
            write_text(root, "profiles/local-laptop/profile.template.json", json.dumps(profile))
            self.assert_has_error(root, "allow_non_loopback is not false")


if __name__ == "__main__":
    unittest.main()
