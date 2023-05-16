class node:
  def __init__(self,data):
    self.data = data
    self.next_node = None
class queue:
    def __init__(self, data=None):
            self.first_node = node(None)

    def pop(self):
        if self.first_node is None:
            return None

        data = self.first_node.data
        self.first_node = self.first_node.next_node
        return data

    
    def append(self, data):
            if self.first_node is None or self.first_node.data is None:
                self.first_node = node(data)
                return