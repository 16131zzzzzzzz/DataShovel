import os
import json
import copy

class TextSolver():
    def __init__(self):
        pass

    def get_newnode(self, text_id):
        """get a new node for text
        """
        new_node = {"nodetype": 0, "id": text_id, "children": []}
        return new_node

    def get_newentry(self, text_id, page, box, content):
        """get a new entry for text
        """
        new_entry = [text_id, page, box, content]
        return new_entry
    
    def get_columns(self):
        """get columns for metacsv
        """
        columns = ["id", "page", "position", "text"]
        return columns
    
class TitleSolver():
    def __init__(self):
        pass

    def get_newnode(self, title_id):
        """get a new node for title
        """
        new_node = {"nodetype": 1, "id": title_id, "children": []}
        return new_node

    def get_newentry(self, title_id, page, box, content):
        """get a new entry for title
        """
        new_entry = [title_id, page, box, content]
        return new_entry

    def get_columns(self):
        """get columns for metacsv
        """
        columns = ["id", "page", "position", "text"]
        return columns
    
class ListSolver():
    def __init__(self):
        pass

    def get_newnode(self, list_id):
        """get a new node for list
        """
        new_node = {"nodetype": 2, "id": list_id, "children": []}
        return new_node

    def get_newentry(self, list_id, page, box, content):
        """get a new entry for list
        """
        new_entry = [list_id, page, box, content]
        return new_entry
    
    def get_columns(self):
        """get columns for metacsv
        """
        columns = ["id", "page", "position", "text"]
        return columns
        
class TableSolver():
    def __init__(self):
        pass

    def get_newnode(self, table_id):
        """get a new node for table
        """
        new_node = {"nodetype": 3, "id": table_id, "children": []}
        return new_node

    def get_newentry(self, table_id, page, box, content):
        """get a new entry for table
        """
        new_entry = [table_id, page, box, content]
        return new_entry

    def get_columns(self):
        """get columns for metacsv
        """
        columns = ["id", "page", "position", "text"]
        return columns

class FigureSolver():
    def __init__(self):
        pass

    def get_newnode(self, figure_id):
        """get a new node for figure
        """
        new_node = {"nodetype": 4, "id": figure_id, "children": []}
        return new_node

    def get_newentry(self, figure_id, page, box, content):
        """get a new entry for figure
        """
        new_entry = [figure_id, page, box, content]
        return new_entry
    
    def get_columns(self):
        """get columns for metacsv
        """
        columns = ["id", "page", "position", "text"]
        return columns