info_from_users = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(users_info: list, state: str = "EXECUTED") -> list:
    """Filtering of user data on executed / canceled operations"""

    new_info = []
    for person_info in users_info:
        if person_info["state"] == state:
            new_info.append(person_info)

    return new_info


if __name__ == "__main__":
    print(filter_by_state(info_from_users, "CANCELED"))
