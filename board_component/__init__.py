import streamlit.components.v1 as components
from pathlib import Path

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "board_component",
        url="http://localhost:5173",
    )
else:
    build_dir = Path(__file__).parent / "frontend" / "dist"

    _component_func = components.declare_component(
        "board_component",
        path=str(build_dir),
    )


def board_component(key=None, **kwargs):
    return _component_func(
        key=key,
        default=None,
        **kwargs,
    )