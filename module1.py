class CommandNode:
    def __init__(self, data):
        self.data = data
        self.next_node = None
        self.previous_node = None


class CommandHistory:
    def __init__(self):
        self.current_node = None
        self.first_node = None
        self.last_node = None
        self.all_commands = []

    def add_command(self, data):
        new_node = CommandNode(data)

        if self.first_node is None:
            self.first_node = new_node

        if self.current_node is not None:
            self.current_node.next_node = new_node
            new_node.previous_node = self.current_node

        self.current_node = new_node
        self.last_node = new_node
        self.all_commands.append(data)

    def get_last_command(self):
        if self.last_node is None:
            return "Pas d'historique"

        return self.last_node.data

    def get_all_commands(self):
        if self.first_node is None:
            return "Pas d'historique"

        commands = []
        current_node = self.first_node
        while current_node is not None:
            commands.append(current_node.data)
            current_node = current_node.next_node

        return commands

    def move_forward(self):
        if self.current_node is None:
            return

        if self.current_node.next_node is not None:
            self.current_node = self.current_node.next_node
        else:
            return "Fin de l'historique"

        return self.current_node.data

    def move_backward(self):
        if self.current_node is None:
            return

        if self.current_node.previous_node is not None:
            self.current_node = self.current_node.previous_node
        else:
            return "Début de l'historique"

        return self.current_node.data

    def clear(self):
        self.current_node = None
        self.first_node = None
        self.last_node = None
        self.all_commands.clear()

    def __str__(self):
        if self.first_node is None:
            return "Pas d'historique"

        commands = []
        current_node = self.first_node
        while current_node is not None:
            commands.append(current_node.data)
            current_node = current_node.next_node

        return "\n".join(commands)

