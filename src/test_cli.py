import json
import unittest
from cli import parser
import io
import sys


def capture_stdout():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    return captured_output


def reset_stdout():
    sys.stdout = sys.__stdout__


def run_cli(arguments: list[str]) -> list[dict] | dict:
    args = parser.parse_args(args=arguments)

    captured_output = capture_stdout()
    args.func(args)
    reset_stdout()

    output = captured_output.getvalue()

    parsed_output = json.loads(output)

    return parsed_output


class TestTask(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        reset_stdout()

    def test_cli(self):
        # Create a habit

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "habits:create",
                "--name",
                "test",
                "--description",
                "test description",
                "--interval",
                "PT4H",
                "--lifetime",
                "PT2H",
                "--active",
                "true",
                "--start",
                "2023-10-24T08:00:00",
                "--end",
                "2023-10-25T08:00:00",
            ]
        )

        self.assertEqual(len(parsed_output), 1)
        self.assertDictEqual(
            parsed_output[0],
            parsed_output[0]
            | {
                "name": "test",
                "description": "test description",
                "interval": "PT4H",
                "lifetime": "PT2H",
                "active": True,
                "start": "2023-10-24T08:00:00",
                "end": "2023-10-25T08:00:00",
            },
        )

        # Store id

        habit_id = parsed_output[0]["id"]

        # list habit

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "habits:list",
                "--id",
                str(habit_id),
            ]
        )

        self.assertEqual(len(parsed_output), 1)
        self.assertDictEqual(
            parsed_output[0],
            {
                "id": habit_id,
                "name": "test",
                "description": "test description",
                "interval": "PT4H",
                "lifetime": "PT2H",
                "active": True,
                "start": "2023-10-24T08:00:00",
                "end": "2023-10-25T08:00:00",
            },
        )

        # List tasks

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "tasks:list",
                "--habit_id",
                str(habit_id),
            ]
        )
        self.assertEqual(len(parsed_output), 6)
        self.assertDictEqual(
            parsed_output[0],
            parsed_output[0]
            | {
                "completed": False,
                "end": "2023-10-24T10:00:00",
                "habit_id": habit_id,
                "habit_order": 1,
                "start": "2023-10-24T08:00:00",
            },
        )
        self.assertDictEqual(
            parsed_output[1],
            parsed_output[1]
            | {
                "completed": False,
                "end": "2023-10-24T14:00:00",
                "habit_id": habit_id,
                "habit_order": 2,
                "start": "2023-10-24T12:00:00",
            },
        )
        self.assertDictEqual(
            parsed_output[2],
            parsed_output[2]
            | {
                "completed": False,
                "end": "2023-10-24T18:00:00",
                "habit_id": habit_id,
                "habit_order": 3,
                "start": "2023-10-24T16:00:00",
            },
        )
        self.assertDictEqual(
            parsed_output[3],
            parsed_output[3]
            | {
                "completed": False,
                "end": "2023-10-24T22:00:00",
                "habit_id": habit_id,
                "habit_order": 4,
                "start": "2023-10-24T20:00:00",
            },
        )
        self.assertDictEqual(
            parsed_output[4],
            parsed_output[4]
            | {
                "completed": False,
                "end": "2023-10-25T02:00:00",
                "habit_id": habit_id,
                "habit_order": 5,
                "start": "2023-10-25T00:00:00",
            },
        )
        self.assertDictEqual(
            parsed_output[5],
            parsed_output[5]
            | {
                "completed": False,
                "end": "2023-10-25T06:00:00",
                "habit_id": habit_id,
                "habit_order": 6,
                "start": "2023-10-25T04:00:00",
            },
        )

        # Save task id
        task_id = parsed_output[0]["id"]

        # Complete task

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "tasks:complete",
                "--id",
                str(task_id),
            ]
        )

        self.assertDictEqual(parsed_output, {"id": task_id})

        # Update habit

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "habits:update",
                "--id",
                str(habit_id),
                "--name",
                "test2",
            ]
        )

        self.assertEqual(len(parsed_output), 1)
        self.assertDictEqual(
            parsed_output[0],
            parsed_output[0]
            | {
                "id": habit_id,
                "name": "test2",
                "description": "test description",
                "interval": "PT4H",
                "lifetime": "PT2H",
                "active": True,
                "start": "2023-10-24T08:00:00",
                "end": "2023-10-25T08:00:00",
            },
        )

        # Analytics list_current_habits

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "analytics",
                "list_current_habits",
                "--habit_id",
                str(habit_id),
            ]
        )

        self.assertDictEqual(
            list(filter(lambda h: h["id"] == habit_id, parsed_output))[0],
            {
                "id": habit_id,
                "name": "test2",
                "description": "test description",
                "interval": "PT4H",
                "lifetime": "PT2H",
                "active": True,
                "start": "2023-10-24T08:00:00",
                "end": "2023-10-25T08:00:00",
            },
        )

        # Analytics list_longest_streaks

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "analytics",
                "list_longest_streaks",
                "--habit_id",
                str(habit_id),
            ]
        )

        self.assertEqual(
            parsed_output, [{"streak": 1, "ids": [task_id], "habit_id": habit_id}]
        )

        # Analytics get_longest_streak

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "analytics",
                "get_longest_streak",
                "--habit_id",
                str(habit_id),
            ]
        )

        self.assertEqual(
            parsed_output, [{"streak": 1, "ids": [task_id], "habit_id": habit_id}]
        )

        # Delete habit

        parsed_output = run_cli(
            [
                "--format",
                "json",
                "habits:delete",
                "--id",
                str(habit_id),
            ]
        )

        self.assertEqual(len(parsed_output), 1)
        self.assertDictEqual(parsed_output[0], {"id": habit_id})


if __name__ == "__main__":
    unittest.main()
