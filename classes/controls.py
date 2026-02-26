"""Action-based input system.

Every input the game cares about is an *action* string (e.g. ``"shoot"``).
Each action maps to one or more keyboard keys and, optionally, joystick
buttons or axes.  Three query functions expose the state each frame:

* ``action_pressed(action)``  – true on the frame the action starts
* ``action_released(action)`` – true on the frame the action stops
* ``action_holding(action)``  – true every frame the action is held

Call ``update(events)`` once per frame **before** any queries.
Joystick is discovered and initialised automatically on the first update.
"""
import pygame

# ── configurable bindings (mutate at runtime for rebinding) ─────────
ACTION_KEYS: dict[str, list[int]] = {
    "up":    [pygame.K_UP,    pygame.K_w],
    "down":  [pygame.K_DOWN,  pygame.K_s],
    "left":  [pygame.K_LEFT,  pygame.K_a],
    "right": [pygame.K_RIGHT, pygame.K_d],
    "shoot": [pygame.K_SPACE, pygame.K_RETURN],
    "pause": [pygame.K_p,     pygame.K_PAUSE],
    "quit":  [pygame.K_ESCAPE],
}

# joystick button index → actions triggered
JOYSTICK_BUTTONS: dict[int, list[str]] = {
    0: ["shoot"],
    7: ["pause"],
}

# joystick axis index → (negative_action, positive_action)
JOYSTICK_AXES: dict[int, tuple[str, str]] = {
    0: ("left",  "right"),
    1: ("up",    "down"),
}

JOYSTICK_DEAD_ZONE = 0.25

# ── joystick (lazy-initialised on first update) ─────────────────────
_joystick: pygame.joystick.JoystickType | None = None
_joystick_checked = False

# ── internal per-frame state ─────────────────────────────────────────
_just_pressed:  set[str] = set()
_just_released: set[str] = set()
_held_joy_btn:  set[str] = set()       # actions held via joystick buttons
_prev_axis:     dict[int, float] = {}  # previous axis values for edge detection

# reverse map: key-code → actions  (rebuild after editing ACTION_KEYS)
_key_to_actions: dict[int, list[str]] = {}


def _rebuild_key_map() -> None:
    _key_to_actions.clear()
    for action, keys in ACTION_KEYS.items():
        for k in keys:
            _key_to_actions.setdefault(k, []).append(action)


_rebuild_key_map()


def _axis_active(axis: int, value: float) -> set[str]:
    """Return directional actions active for a given axis value."""
    neg, pos = JOYSTICK_AXES.get(axis, (None, None))
    active: set[str] = set()
    if neg and value < -JOYSTICK_DEAD_ZONE:
        active.add(neg)
    if pos and value > JOYSTICK_DEAD_ZONE:
        active.add(pos)
    return active


# ── public API ───────────────────────────────────────────────────────

def update(events: list[pygame.event.Event]) -> None:
    """Process one frame of events.  Call once per frame, before queries."""
    global _joystick, _joystick_checked

    # lazy joystick init
    if not _joystick_checked:
        _joystick_checked = True
        if pygame.joystick.get_count() > 0:
            _joystick = pygame.joystick.Joystick(0)
            _joystick.init()

    _just_pressed.clear()
    _just_released.clear()

    # --- axis edge detection (pressed / released from axis crossings) ---
    if _joystick is not None:
        for axis_idx in JOYSTICK_AXES:
            current = _joystick.get_axis(axis_idx)
            prev = _prev_axis.get(axis_idx, 0.0)
            was = _axis_active(axis_idx, prev)
            now = _axis_active(axis_idx, current)
            _just_pressed.update(now - was)
            _just_released.update(was - now)
            _prev_axis[axis_idx] = current

    # --- keyboard & joystick button events ---
    for event in events:
        if event.type == pygame.KEYDOWN:
            for action in _key_to_actions.get(event.key, ()):
                _just_pressed.add(action)

        elif event.type == pygame.KEYUP:
            for action in _key_to_actions.get(event.key, ()):
                _just_released.add(action)

        elif event.type == pygame.JOYBUTTONDOWN:
            for action in JOYSTICK_BUTTONS.get(event.button, ()):
                _just_pressed.add(action)
                _held_joy_btn.add(action)

        elif event.type == pygame.JOYBUTTONUP:
            for action in JOYSTICK_BUTTONS.get(event.button, ()):
                _just_released.add(action)
                _held_joy_btn.discard(action)

        elif event.type == pygame.JOYHATMOTION:
            _, hy = event.value
            if hy == 1:
                _just_pressed.add("up")
            elif hy == -1:
                _just_pressed.add("down")


def action_pressed(action: str) -> bool:
    """True on the single frame the action was triggered."""
    return action in _just_pressed


def action_released(action: str) -> bool:
    """True on the single frame the action was released."""
    return action in _just_released


def action_holding(action: str) -> bool:
    """True every frame the action is held down."""
    # joystick axes → digital check
    if _joystick is not None:
        for axis_idx, (neg, pos) in JOYSTICK_AXES.items():
            val = _joystick.get_axis(axis_idx)
            if action == neg and val < -JOYSTICK_DEAD_ZONE:
                return True
            if action == pos and val > JOYSTICK_DEAD_ZONE:
                return True
    # joystick buttons
    if action in _held_joy_btn:
        return True
    # keyboard
    keys = pygame.key.get_pressed()
    return any(keys[k] for k in ACTION_KEYS.get(action, ()))


def get_movement() -> tuple[int, int]:
    """Return (x, y) as integer -1/0/+1 from directional actions."""
    x = int(action_holding("right")) - int(action_holding("left"))
    y = int(action_holding("down"))  - int(action_holding("up"))
    return x, y
