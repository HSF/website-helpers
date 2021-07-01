# std
from pathlib import Path

# 3rd
import pytest

# ours
from hsf_website_helpers.profiles.profile import Profile


@pytest.fixture()
def test_profile() -> Profile:
    this_dir = Path(__file__).resolve().parent
    test_file = this_dir / "test_profile.md"
    p = Profile.from_file(test_file)
    return p


def test_profile_read(test_profile):
    p = test_profile
    assert p.header["title"] == "Kilian Lieret"
    assert p.header["country"] == "DE"
    assert p.header["training_roles"] == []
    assert p.header["training_years"] == [2020]
    assert p.header["github"] == "klieret"
    assert p.header["gitlab"] == "klieret"
    assert p.header["homepage"] == "https://lieret.net"
    assert p.header["orcid"] == "0000-0003-2792-7511"
    assert (
        p.content == "Hi, I'm Kilian. I'm a PhD student for the Belle II "
        "experiment and joined the HSF training group in 2020."
    )


def test_profile_to_from_identical(test_profile, tmp_path):
    p = test_profile
    target = tmp_path / "test.md"
    p.to_file(target)
    p_circular = Profile.from_file(target)
    assert p_circular.header == p.header
    assert p_circular.content == p.content


def test_same_person_idential(test_profile):
    assert test_profile.same_person(test_profile)
