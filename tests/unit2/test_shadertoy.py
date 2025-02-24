import pytest
from arcade.experimental import Shadertoy, ShadertoyBuffer
from arcade.gl import Program, Texture

def glsl(inner: str):
    return (
        "void mainImage(out vec4 fragColor, in vec2 fragCoord)\n"
        "{\n"
        f"{inner}\n"
        "}\n"
    )


def test_create_from_file(ctx):
    st = Shadertoy.create_from_file((100, 200), ":resources:shaders/shadertoy/crt_monitor_filter.glsl")
    check_internals(st)

    with pytest.raises(FileNotFoundError):
        st = Shadertoy.create_from_file((100, 200), "something.glsl")

def test_create(ctx):
    st = Shadertoy((120, 130), glsl("fragColor = vec4(1.0, 1.0, 1.0, 1.0);"))
    check_internals(st)

def test_buffers(ctx):
    st = Shadertoy((120, 130), glsl("fragColor = vec4(1.0, 1.0, 1.0, 1.0);"))
    buffer_a = st.create_buffer(glsl("fragColor = vec4(1.0, 0.0, 0.0, 1.0);"))
    buffer_b = st.create_buffer(glsl("fragColor = vec4(0.0, 1.0, 0.0, 1.0);"))
    buffer_c = st.create_buffer(glsl("fragColor = vec4(0.0, 0.0, 1.0, 1.0);"))
    buffer_d = st.create_buffer(glsl("fragColor = vec4(0.0, 0.0, 0.0, 1.0);"))
    st.buffer_a = buffer_a
    st.buffer_b = buffer_b
    st.buffer_c = buffer_c
    st.buffer_d = buffer_d
    assert st.buffer_a == buffer_a
    assert st.buffer_b == buffer_b
    assert st.buffer_c == buffer_c
    assert st.buffer_d == buffer_d

    buffer_a = ShadertoyBuffer(st.size, glsl("fragColor = vec4(1.0, 0.0, 0.0, 1.0);"))
    buffer_b = ShadertoyBuffer(st.size, glsl("fragColor = vec4(0.0, 1.0, 0.0, 1.0);"))
    buffer_c = ShadertoyBuffer(st.size, glsl("fragColor = vec4(0.0, 0.0, 1.0, 1.0);"))
    buffer_d = ShadertoyBuffer(st.size, glsl("fragColor = vec4(0.0, 0.0, 0.0, 1.0);"))
    st.buffer_a = buffer_a
    st.buffer_b = buffer_b
    st.buffer_c = buffer_c
    st.buffer_d = buffer_d
    assert st.buffer_a == buffer_a
    assert st.buffer_b == buffer_b
    assert st.buffer_c == buffer_c
    assert st.buffer_d == buffer_d

def check_internals(st: Shadertoy):
    assert isinstance(st.program, Program)
    assert isinstance(st.size, tuple)
    assert len(st.size) == 2

    # Default values
    assert st.time == 0
    assert st.time_delta == 0
    assert st.frame == 0
    assert st.mouse_position == (0, 0)

    # Types assigned to channels
    assert st.channel_0 is None or isinstance(st.channel_0, Texture)
    assert st.channel_1 is None or isinstance(st.channel_1, Texture)
    assert st.channel_2 is None or isinstance(st.channel_2, Texture)
    assert st.channel_3 is None or isinstance(st.channel_3, Texture)
