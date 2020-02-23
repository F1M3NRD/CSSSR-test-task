import unittest
import requests

response = requests.get("https://superhero.qa-test.csssr.com/v2/api-docs")
swagger_json = response.json()


def get_all_superheroes(endpoint):
    response = requests.get(endpoint)
    return response


def get_hero_by_id(endpoint):
    response = requests.get(endpoint)
    return response


def post_superhero(endpoint, dict_data):
    response = requests.post(endpoint, json=dict_data)
    return response


def put_superhero(endpoint, dict_data):
    response = requests.put(endpoint, json=dict_data)
    return response


def delete_superhero(endpoint):
    response = requests.delete(endpoint)
    return response


class TestTaskCSSSR(unittest.TestCase):

    def test_get_all_superheroes(self):
        actual_result = get_all_superheroes("https://superhero.qa-test.csssr.com/superheroes")
        self.assertEqual(200, actual_result.status_code)

    def test_get_hero_by_id(self):
        all_superheroes = get_all_superheroes("https://superhero.qa-test.csssr.com/superheroes")
        self.assertEqual(200, all_superheroes.status_code)
        get_id = all_superheroes.json()[-1]["id"]
        actual_result = get_hero_by_id("https://superhero.qa-test.csssr.com/superheroes/{id}".format(id=get_id))
        self.assertEqual(200, actual_result.status_code)
        self.assertEqual(all_superheroes.json()[-1]["fullName"], actual_result.json()["fullName"])

    def test_create_hero(self):
        actual_result = post_superhero("https://superhero.qa-test.csssr.com/superheroes", dict_data={
            "birthDate": "2222-03-15",
            "city": "Testdsa city",
            "gender": "smth",
            "fullName": "2020 current CSSSR task",
            "mainSkill": "test magic",
            "phone": "+123456789"
        })
        self.assertEqual(200, actual_result.status_code)
        get_created_hero = actual_result.json()
        self.assertEqual("2020 current CSSSR task", get_created_hero["fullName"])
        get_id_of_created_hero = get_created_hero["id"]
        hero_is_exist = get_hero_by_id(
            "https://superhero.qa-test.csssr.com/superheroes/{id}".format(id=get_id_of_created_hero))
        self.assertEqual(200, hero_is_exist.status_code)

    def test_update_hero(self):
        create_hero = post_superhero("https://superhero.qa-test.csssr.com/superheroes", dict_data={
            "birthDate": "2222-03-15",
            "city": "Testdsa city",
            "gender": "smth",
            "fullName": "2020 current CSSSR task",
            "mainSkill": "test magic",
            "phone": "+123456789"
        })
        actual_result = put_superhero(
            "https://superhero.qa-test.csssr.com/superheroes/{id}".format(id=create_hero.json()["id"]), dict_data={
                "birthDate": "2222-03-15",
                "city": "Testdsa city",
                "gender": "MUJIK",
                "fullName": "2020 current CSSSR task",
                "mainSkill": "test magic",
                "phone": "+123456789"
            })
        self.assertEqual(200, actual_result.status_code)
        get_updated_hero = get_hero_by_id(
            "https://superhero.qa-test.csssr.com/superheroes/{id}".format(id=create_hero.json()["id"]))
        self.assertEqual(200, get_updated_hero.status_code)
        self.assertEqual("MUJIK", get_updated_hero.json()["gender"])

    def test_delete_hero(self):
        create_hero = post_superhero("https://superhero.qa-test.csssr.com/superheroes", dict_data={
            "birthDate": "2222-03-15",
            "city": "Testdsa city",
            "gender": "smth",
            "fullName": "2020 current CSSSR task",
            "mainSkill": "test magic",
            "phone": "+123456789"
        })
        self.assertEqual(200, create_hero.status_code)
        actual_result = delete_superhero(
            "https://superhero.qa-test.csssr.com/superheroes/{id}".format(id=create_hero.json()["id"]))
        self.assertEqual(200, actual_result.status_code)
        re_delete = delete_superhero(
            "https://superhero.qa-test.csssr.com/superheroes/{id}".format(id=create_hero.json()["id"]))
        self.assertEqual(404, re_delete.status_code)


if __name__ == '__main__':
    unittest.main()
