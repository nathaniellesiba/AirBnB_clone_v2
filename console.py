#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB project"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''


    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    
    def do_EOF(self, line):
        """Exit the command interpreter when EOF is reached"""
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def do_quit(self, line):
        """Exit the command interpreter"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")


    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")


"""---------CRUD--------------"""

    def do_create(self, args):
        """ Create an object of any class"""
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(name_pattern, args)
        obj_kwargs = {}
        if class_match is not None:
            class_name = class_match.group('name')
            params_str = args[len(class_name):].strip()
            params = params_str.split(' ')
            str_pattern = r'(?P<t_str>"([^"]|\")*")'
            float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
            int_pattern = r'(?P<t_int>[-+]?\d+)'
            param_pattern = '{}=({}|{}|{})'.format(
                name_pattern,
                str_pattern,
                float_pattern,
                int_pattern
            )
            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match is not None:
                    key_name = param_match.group('name')
                    str_v = param_match.group('t_str')
                    float_v = param_match.group('t_float')
                    int_v = param_match.group('t_int')
                    if float_v is not None:
                        obj_kwargs[key_name] = float(float_v)
                    if int_v is not None:
                        obj_kwargs[key_name] = int(int_v)
                    if str_v is not None:
                        obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
        else:
            class_name = args
        if not class_name:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if not hasattr(obj_kwargs, 'id'):
                obj_kwargs['id'] = str(uuid.uuid4())
            if not hasattr(obj_kwargs, 'created_at'):
                obj_kwargs['created_at'] = str(datetime.now())
            if not hasattr(obj_kwargs, 'updated_at'):
                obj_kwargs['updated_at'] = str(datetime.now())
            new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
            new_instance.save()
            print(new_instance.id)
        else:
            new_instance = HBNBCommand.classes[class_name]()
            for key, value in obj_kwargs.items():
                if key not in ignored_attrs:
                    setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

"""-----------loops---------------"""


    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] is '{' and pline[-1] is'}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop



if __name__ == '__main__':
    HBNBCommand().cmdloop()
