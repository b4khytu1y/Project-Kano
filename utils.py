import json
from pathlib import Path
from typing import List, Dict, Iterable

DATA_FILE = Path('tasks.json')


def load_tasks() -> Dict[str, List[str]]:
    if DATA_FILE.exists():
        with DATA_FILE.open('r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_tasks(tasks: Dict[str, List[str]]) -> None:
    with DATA_FILE.open('w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(user_id: int, task: str) -> None:
    tasks = load_tasks()
    user_tasks = tasks.get(str(user_id), [])
    user_tasks.append(task)
    tasks[str(user_id)] = user_tasks
    save_tasks(tasks)


def get_user_tasks(user_id: int) -> List[str]:
    tasks = load_tasks()
    return tasks.get(str(user_id), [])


def get_all_users() -> Iterable[int]:
    tasks = load_tasks()
    return [int(uid) for uid in tasks.keys()]
