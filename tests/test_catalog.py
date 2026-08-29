"""The catalog itself must stay well formed."""

import pytest

from earlywarn.catalog import CATALOG, IDEAS, by_idea, get, ideas, validate


def test_catalog_has_no_structural_problems():
    assert validate() == []


def test_dataset_ids_are_unique():
    dataset_ids = [source.dataset_id for source in CATALOG]
    assert len(dataset_ids) == len(set(dataset_ids))


def test_every_idea_has_at_least_one_source():
    for idea in ideas():
        assert by_idea(idea), f"{idea} has no sources"


def test_by_idea_without_argument_returns_everything():
    assert len(by_idea()) == len(CATALOG)


def test_by_idea_returns_only_that_idea():
    for idea in ideas():
        assert {source.idea for source in by_idea(idea)} == {idea}


def test_get_finds_a_source_and_rejects_unknown_ids():
    assert get("opendengue").provider.startswith("OpenDengue")
    with pytest.raises(KeyError):
        get("no_such_dataset")


def test_access_class_matches_the_fields_it_summarises():
    for source in CATALOG:
        if source.fetchable:
            assert source.access_class == "auto"
        elif source.auth_required.startswith("yes"):
            assert source.access_class == "key"
        else:
            assert source.access_class == "manual"


def test_fetchable_sources_have_a_download_url():
    for source in CATALOG:
        if source.fetchable:
            assert source.download_url.startswith("http")


def test_idea_labels_cover_every_idea_used():
    assert {source.idea for source in CATALOG} <= set(IDEAS)
