"""This is a wrapper around the callback based event model which uses
a global-event style."""

import streamlit as st
from typing import Optional, Any, Union
import functools


#######################
# Global event object #
#######################

# This is a sentinal meaning that no signal has been recieved
class NoSignal:
    pass
_no_signal = NoSignal


# This is the label of the last event that just fired
_event_signal: Optional[Union[str, NoSignal]] = _no_signal


# This is the value of the last event that just fired
_event_value: Any = None


# Optionally, the user may set a "context" for an event, which is simply
# additional information which will be made available when the event fires.
# You can think of this a closure for this signal-based event model.
_event_context: Any = None


def _wrap_widget(widget_func, callback_label):
    """Wraps a widget so that it uses the global event object above."""

    @functools.wraps(widget_func)
    def wrapped_widget(label, *args, signal=None, context=None, **kwargs):
        """This is a version of the wrapped Streamlit object which uses the
        global even object above."""

        def generic_callback(*args):
            """Generic callback for any widget."""
            global _event_signal, _event_value, _event_context

            # Set the global event signal
            if signal is None:
                _event_signal = label
            else:
                _event_signal = signal

            # Set the global event value
            if len(args) == 0:
                _event_value = None
            elif len(args) == 1:
                _event_value = args[0]
            else:
                err_str = f"Not expecting a callback with {len(args)} args."
                raise RuntimeError(err_str)

            # Set the global even context
            _event_context = context

        # Actually create the widget now
        widget_kwargs = dict(kwargs)
        widget_kwargs[callback_label] = generic_callback
        return widget_func(label, *args, **widget_kwargs)

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

def no_signal() -> bool:
    """Returns true if no signal has been fired."""
    return _event_signal == _no_signal

def signal(signal: str) -> bool:
    """Returns true if the widget with the given signal changed."""
    return _event_signal == signal

def value() -> Any:
    """Returns the value of the event."""
    return _event_value

def context() -> Any:
    """Returns the context for the event."""
    return _event_context
