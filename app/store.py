class InMemoryStore:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def create(self, title, owner):
        task = {"id": self.next_id, "title": title, "owner": owner, "completed": False}
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get(self, task_id):
        return self.tasks.get(task_id)

    def list_for(self, owner):
        return [t for t in self.tasks.values() if t["owner"] == owner]

    def delete(self, task_id):
        return self.tasks.pop(task_id, None) is not None

store = InMemoryStore()
