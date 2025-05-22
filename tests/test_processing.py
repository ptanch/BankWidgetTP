from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_user_info() -> List[Dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.mark.parametrize("state, expected_ids", [
    ("EXECUTED", [41428829, 939719570]),
    ("CANCELED", [594226727, 615064591]),
])
def test_filter_by_state_valid(sample_user_info: List[Dict], state: str, expected_ids: List[int]) -> None:
    filtered = filter_by_state(sample_user_info, state)
    result_ids = [entry["id"] for entry in filtered]
    assert result_ids == expected_ids


def test_filter_by_state_no_matches(sample_user_info: List[Dict]) -> None:
    result = filter_by_state(sample_user_info, "UNKNOWN")
    assert result == []


def test_filter_by_state_default(sample_user_info: List[Dict]) -> None:
    result = filter_by_state(sample_user_info)
    assert all(entry["state"] == "EXECUTED" for entry in result)


#  тестирование функции sort_by_date
@pytest.fixture
def sample_dates() -> List[Dict]:
    return [
        {"id": 1, "date": "2022-01-03T10:00:00"},
        {"id": 2, "date": "2021-12-31T23:59:59"},
        {"id": 3, "date": "2023-07-15T15:45:30"},
    ]


@pytest.fixture
def same_dates() -> List[Dict]:
    return [
        {"id": 1, "date": "2022-05-01T12:00:00"},
        {"id": 2, "date": "2022-05-01T12:00:00"},
        {"id": 3, "date": "2022-05-01T12:00:00"},
    ]


@pytest.fixture
def invalid_date_format() -> List[Dict]:
    return [
        {"id": 1, "date": "15-07-2023 15:45:30"},
        {"id": 2, "date": "2022/01/03 10:00:00"},
    ]


@pytest.fixture
def partially_valid_dates() -> List[Dict]:
    return [
        {"id": 1, "date": "2022-01-01T00:00:00"},
        {"id": 2, "date": "bad-date-format"},
    ]


@pytest.mark.parametrize("descending, expected_ids", [
    (True, [3, 1, 2]),
    (False, [2, 1, 3]),
])
def test_sort_by_date_order(sample_dates: List[Dict], descending: bool, expected_ids: List[int]) -> None:
    result = sort_by_date(sample_dates, descending=descending)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_ids


def test_sort_by_date_same_values(same_dates: List[Dict]) -> None:
    result = sort_by_date(same_dates)
    result_ids = [item["id"] for item in result]
    assert result_ids == [1, 2, 3]


@pytest.mark.parametrize("bad_data", [
    [{"id": 1, "date": "not-a-date"}],
    [{"id": 1, "date": "2022/01/03"}],
    [{"id": 1, "date": ""}],
])
def test_sort_by_date_invalid_format_raises(bad_data: List[Dict]) -> None:
    with pytest.raises(ValueError):
        sort_by_date(bad_data)


def test_sort_by_date_partial_invalid(partially_valid_dates: List[Dict]) -> None:
    with pytest.raises(ValueError):
        sort_by_date(partially_valid_dates)
