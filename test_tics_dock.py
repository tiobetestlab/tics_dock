import tics_dock
import unittest
import yaml
from unittest.mock import MagicMock, patch
import os



class TestDock(unittest.TestCase):
    def test_load_config_empty(self):
        
        tools, url = tics_dock.load_config('')
        
        self.assertEqual(tools, {})
        self.assertEqual(url, 'http://localhost')


    def test_load_config_existing(self):
        tools, url = tics_dock.load_config('tics_dock_test.cfg')
        
        self.assertEqual(tools, [{'name': 'Eclipse', 'path': 'D:/Tools/Eclipse-2019-09/eclipse/eclipse.exe'},
                                 {'name': 'Visual Studio Code', 'path': 'C:/Users/marvi/AppData/Local/Programs/Microsoft VS Code/Code.exe'}])
        self.assertEqual(url, 'http://localhost:42506/tiobeweb/TICS')

    @patch('yaml.load')
    @patch('sys.exit')
    @patch('tkinter.messagebox.showerror')
    def test_load_config_no_url(self, load, exit, showerror):
        load.return_value = {'TOOLS'}
        tools, url = tics_dock.load_config('tics_dock_test.cfg')
        
        assert showerror.called
        assert exit.called

    @patch('yaml.load')
    @patch('sys.exit')
    @patch('tkinter.messagebox.showerror')
    def test_load_config_no_tools(self, load, exit, showerror):
        load.return_value = {'TICS_VIEWER_URL'}
        _, _ = tics_dock.load_config('tics_dock_test.cfg')
        
        assert showerror.called
        assert exit.called

    @patch('tics_dock.main')
    def test_save_config(self, main):
        mock_data = {'I001': {'values': ['name_a', 'path_a']},
                     'I002': {'values': ['name_b', 'path_b']}}
        
        tree = StubTree()
        tics_url = StubObject()
        cfg_file = 'tics_dock_test_write.cfg'
        root = StubObject()
        
        tics_url.set('http://watbenjedan.nl')
        tree.children = mock_data
        
        tics_dock.save_config(tree, tics_url, cfg_file, root)
        
        with open(cfg_file) as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        
        self.assertEqual(config['TOOLS']['name_a'], 'path_a')
        self.assertEqual(config['TOOLS']['name_b'], 'path_b')
        
        assert main.called

    def test_tree_select(self):
        
        mock_data = {'I001': {'values': ['name_a', 'path_a']},
                     'I002': {'values': ['name_b', 'path_b']}}
        mock_key = 'I002'
        
        tree = StubTree()
        tree.set_children(mock_data)
        tree.selected = mock_key
        
        new_name = StubObject()
        new_path = StubObject()
        
        tics_dock.tree_select(tree, new_name, new_path)
        
        self.assertEqual(new_name.value, mock_data[mock_key]['values'][0])
        self.assertEqual(new_path.value, mock_data[mock_key]['values'][1])


    def test_close_window(self):
        window = StubObject()
        tics_dock.close_window(window)
        
        self.assertEqual(window.destroyed, True)


    def test_insert_new(self):
        mock_data = {'I001': {'values': ['name_a', 'path_a']},
                     'I002': {'values': ['name_b', 'path_b']}}

        tree = StubTree()
        new_name = StubObject()
        new_path = StubObject()
        
        tree.set_children(mock_data)
        tree.selected = None
        tree.index_value = 3
        new_name.set('name_c')
        new_path.set('path_c')
        cfg_window = None
        
        tics_dock.insert(tree, new_name, new_path, cfg_window)
        
        self.assertEqual(tree.children['I003']['values'][0], 'name_c')
        self.assertEqual(tree.children['I003']['values'][1], 'path_c')

    def test_insert_update(self):
        mock_data = {'I001': {'values': ['name_a', 'path_a']},
                     'I002': {'values': ['name_b', 'path_b']}}

        tree = StubTree()
        new_name = StubObject()
        new_path = StubObject()
        
        tree.set_children(mock_data)
        tree.selected = 'I002'
        tree.index_value = 2
        new_name.set('name_b')
        new_path.set('path_c')
        cfg_window = None
        
        tics_dock.insert(tree, new_name, new_path, cfg_window)
        
        self.assertEqual(tree.children['I002']['values'][0], 'name_b')
        self.assertEqual(tree.children['I002']['values'][1], 'path_c')

    @patch('tkinter.messagebox.showerror')
    def test_insert_duplicate(self, showerror):
        mock_data = {'I001': {'values': ['name_a', 'path_a']},
                     'I002': {'values': ['name_b', 'path_b']}}

        tree = StubTree()
        new_name = StubObject()
        new_path = StubObject()
        
        tree.set_children(mock_data)
        tree.selected = None
        tree.index_value = 2
        new_name.set('name_b')
        new_path.set('path_b')
        cfg_window = None
        
        tics_dock.insert(tree, new_name, new_path, cfg_window)
        
        self.assertEqual(tree.children['I002']['values'][0], 'name_b')
        self.assertEqual(tree.children['I002']['values'][1], 'path_b')
        assert showerror.called

    @patch('tkinter.messagebox.showerror')
    def test_insert_empty_name(self, showerror):
        tree = StubTree()
        new_name = StubObject()
        new_path = StubObject()

        new_name.set('')
        new_path.set('path')
        cfg_window = None
        
        tics_dock.insert(tree, new_name, new_path, cfg_window)
        
        assert showerror.called
    
    @patch('tkinter.messagebox.showerror')
    def test_insert_empty_path(self, showerror):
        tree = StubTree()
        new_name = StubObject()
        new_path = StubObject()

        new_name.set('name')
        new_path.set('')
        cfg_window = None
        
        tics_dock.insert(tree, new_name, new_path, cfg_window)
        
        assert showerror.called


    def test_remove(self):
        mock_data = {'I001': {'values': ['name_a', 'path_a']},
                     'I002': {'values': ['name_b', 'path_b']}}
        mock_key = ['I002']
        
        tree = StubTree()
        tree.set_children(mock_data)
        tree.selected = mock_key
        
        tics_dock.remove(tree)
        
        self.assertEqual(len(tree.children.keys()), 1)

    @patch('tkinter.messagebox.showerror')
    @patch('sys.exit')
    def test_inform_and_die(self, showerror, exit):
        tics_dock.inform_and_die('test_error', 'This is a test')
        assert showerror.called
        assert exit.called

    @patch('tkinter.filedialog.askopenfilename')
    def test_open_file(self, askopenfilename):
        name_obj = StubObject()
        path_obj = StubObject() 
        
        askopenfilename.return_value = 'C:/mock/stub.exe'
        tics_dock.open_file(name_obj, path_obj, None)
        
        assert askopenfilename.called
        self.assertEqual(name_obj.value, 'Stub')
        self.assertEqual(path_obj.value, 'C:/mock/stub.exe')

    @patch('os.startfile')
    @patch('sys.platform', 'win32')
    def test_run_url_win32(self, startfile):
        tics_dock.run_tics_viewer('http://watbenjedan.nl')
        
        assert startfile.called
    
    @patch('sys.platform', 'linux')
    @patch('subprocess.call')
    def test_run_url_linux(self, call):
        tics_dock.run_tics_viewer('http://watbenjedan.nl')
        
        assert call.called

    @patch('tkinter.messagebox.showerror')
    def test_run_invalid_url_win32(self, showerror):
        tics_dock.run_tics_viewer('watbenjedan')

        assert showerror.called

    @patch('tkinter.messagebox.showerror')
    def test_run_tool_invalid(self, showerror):
        
        tics_dock.run_tool('')
        
        assert showerror.called
    
    @patch('os.startfile')
    @patch('sys.platform', 'win32')
    def test_run_tool_win32(self, startfile):
        
        tics_dock.run_tool(os.path.basename(__file__))
        
        assert startfile.called
    
    @patch('subprocess.Popen')
    @patch('sys.platform', 'linux')
    def test_run_tool_linux(self, Popen):
        
        tics_dock.run_tool(os.path.basename(__file__))
        
        assert Popen.called
    
    @patch('os.startfile')
    @patch('sys.platform', 'win32')
    def test_run_tool_url(self, startfile):
        
        tics_dock.run_tool('http://watbenjedan.nl')
        
        assert startfile.called
    
    def test_is_url(self):
        
        ret_val1 = tics_dock.is_url('http://watbenjedan.nl') != None
        ret_val2 = tics_dock.is_url('watbenjedan') == None
        
        self.assertEqual(ret_val1, True)
        self.assertEqual(ret_val2, True)


class StubObject():
    value = ''
    children = ''
    selected = ''
    position = 0
    destroyed = False
    index = 0
    
    def get(self):
        return self.value

    def set(self, new_value):
        self.value = new_value
    
    def destroy(self):
        self.destroyed = True

    def delete(self, start_idx, end_idx=None):
        pass
    
    def insert(self, position, value):
        self.position = position
        self.value = value


class StubTree(StubObject):
    text = ''
    value = ''
    children = ''
    selected = ''
    position = 0
    destroyed = False
    index_value = 0

    def get_children(self):
        return self.children
    
    def set_children(self, new_children):
        self.children = new_children
    
    def item(self, item_key, element=''):
        if element:
            return self.children[item_key][element]
        else:
            return self.children[item_key]
    
    def selection(self):
        return self.selected
    
    def index(self, indexed_item):
        return self.index_value
    
    def focus(self):
        return None
    
    def insert(self, start, position, text='', values=[]):
        new_key = f'I00{position}'
        self.children[new_key]={'values': values}
        
    def delete(self, key_to_remove):
        self.children.pop(key_to_remove, None)
    
    
    

if __name__ == '__main__':
    unittest.main()