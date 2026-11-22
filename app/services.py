def normalize_title(title):
    return " ".join(title.strip().split())

def create_task(store, title, owner):
    title = normalize_title(title)
    if not title:
        raise ValueError("title cannot be empty")
    if len(title) > 120:
        raise ValueError("title is too long")
    return store.create(title, owner)

def complete_task(store, task_id, owner):
    task = store.get(task_id)
    if task is None:
        raise LookupError("task not found")
    if task["owner"] != owner:
        raise PermissionError("not task owner")
    task["completed"] = True
    return task
