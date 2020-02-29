from concurrent.futures import ThreadPoolExecutor
from tester import Tester

if __name__ == "__main__":

    schema = {
        "first_name": {"data_type": "first_name"},
        "last_name": {"data_type": "last_name"},
        "telegram_id": {"default_value": None},
        "telegram_chat_id": {"default_value": None},
        "referring_user_id": {"data_type": "recursive_relation", "transform": lambda x: str(x) if x is not None else x}
    }

    url = "192.168.0.29:4000"

    with ThreadPoolExecutor(max_workers=5) as executor:
        MembershipTester1 = Tester(url)
        MembershipTester1.set_schema("/signup", schema, Tester.METHOD_PUT)

        executor.submit(lambda: MembershipTester1.run_all(100))
