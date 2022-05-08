"""
this library contains unrelated functions and classes
"""

import inspect
import typing

def get_caller_name() -> str:
    """ 
    returns the name of the calling method

    Returns:
        str: name of the calling method
    """
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    calling_method_name = calframe[1][3]
    return calling_method_name

def get_caller_class():
    stack = inspect.stack()
    calling_class = stack[2][0].f_locals['self']
    return calling_class

def caller_hasattr(attr: str, deep:bool = False) -> bool:
    """
    checks if the caller class has an attribute
    """
    stack = inspect.stack()
    calling_stack = stack[2][0].f_locals
    # find local scope
    if attr in calling_stack:
        return True
    # find in instance scope
    if (instance:=calling_stack.get("self", None)) is not None and hasattr(instance, attr):
        return True
    # find in class scope
    if (cls:=calling_stack.get("cls", None)) is not None and hasattr(cls, attr):
        return True
    # deep scope
    if deep:
        for k, v in calling_stack.items():
            if v is None:
                continue
            elif isinstance(v, dict):
                if attr in v:
                    return True
            elif isinstance(v, typing.Iterable):
                continue
            elif isinstance(v, (int, float, str, bool)):
                continue
            elif hasattr(v, attr):
                return True
    
    return False

def caller_getattr(attr: str, default =None, deep: bool = False) -> object:
    """
    returns the attribute of the caller class
    """
    stack = inspect.stack()
    calling_stack = stack[2][0].f_locals
    # find local scope
    if attr in calling_stack:
        return calling_stack[attr]
    # find in instance scope
    if (instance:=calling_stack.get("self", None)) is not None and hasattr(instance, attr):
        return getattr(instance, attr, default)
    # find in class scope
    if (cls:=calling_stack.get("cls", None)) is not None and hasattr(cls, attr):
        return getattr(cls, attr, default)
    # deep scope
    if deep:
        for k, v in calling_stack.items():
            if v is None:
                continue
            elif isinstance(v, dict):
                if attr in v:
                    return v[attr]
            elif isinstance(v, typing.Iterable):
                continue
            elif isinstance(v, (int, float, str, bool)):
                continue
            elif hasattr(v, attr):
                return getattr(v, attr, default)

    return default
