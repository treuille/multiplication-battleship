"""This is a wrapper around the callback based event model which uses
a global-event style."""

import streamlit as st
from typing import Optional, Any
import functools


#######################
# Global event object #
#######################


# This is the label of the last event that just fired
_event_key: Optional[str] = None


# This is the value of the last event that just fired
_event_value: Any = None


def _wrap_widget(widget_func, callback_label):
    """Wraps a widget so that it uses the global event object above."""

    @functools.wraps(widget_func)
    def wrapped_widget(*args, key=None, **kwargs):
        """This is a version of the wrapped Streamlit object which uses the
        global even object above."""

        # Becuase we use the key to figure out which widget fired, it cannot be
        # none.
        if key == None:
            raise RuntimeError("Must specify the key.")

        def generic_callback(*args):
            """Generic callback for any widget."""
            global _event_key, _event_value

            # Set the global event value
            if len(args) == 0:
                _event_value = None
            elif len(args) == 1:
                _event_value = args[0]
            else:
                err_str = f"Not expecting a callback with {len(args)} args."
                raise RuntimeError(err_str)

            # Set the global event key
            _event_key = key

        # Actually create the widget now
        widget_kwargs = dict(kwargs)
        widget_kwargs["key"] = key
        widget_kwargs[callback_label] = generic_callback
        return widget_func(*args, **widget_kwargs)

    return wrapped_widget

###########
# Widgets # 
###########

text_input = _wrap_widget(st.text_input, "on_change")
number_input = _wrap_widget(st.number_input, "on_change")
button = _wrap_widget(st.button, "on_click")


########################
# API to get the event #
########################

def changed(key: str) -> bool:
    """Returns true if the widget with the given key changed."""
    return _event_key == key

def value() -> Any:
    """Returns the value of the event."""
    return _event_value
