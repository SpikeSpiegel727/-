class Task:
    def __init__(self, name, priority, duration, deadline):
        self.name = name
        self.priority = priority       # 1 - высокий, 2 - средний, 3 - низкий
        self.duration = duration       # время выполнения в часах
        self.deadline = deadline       # объект datetime

    def to_string(self, priority_names):
        deadline_str = self.deadline.strftime("%d.%m.%Y")
        return (
            "Задача: " + self.name +
            " | Приоритет: " + priority_names[self.priority] +
            " | Время: " + str(self.duration) + " ч" +
            " | Дедлайн: " + deadline_str
        )
