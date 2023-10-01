import numpy as np
import time
import keyboard

SCREEN_SIZE = 40
THETA_SPACING = 0.07
PHI_SPACING = 0.02
ILLUMINATION_CHARS = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

rotation_A = 1
rotation_B = 1
inner_radius = 0.9  
outer_radius = 1.8  
projection_plane_distance = 5
projection_plane_scaling = SCREEN_SIZE * projection_plane_distance * 3 / (8 * (inner_radius + outer_radius))

ZOOM_SPEED = 0.1  # Controls the speed of zooming

class TerminalColors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"


def map_char_to_color(char: str) -> str:
    char_color_mappings = {
        ".,-": TerminalColors.BLUE,
        "~:;": TerminalColors.CYAN,
        "=!*": TerminalColors.YELLOW,
        "#$@": TerminalColors.RED,
    }
    for chars, color in char_color_mappings.items():
        if char in chars:
            return color
    return TerminalColors.RESET



def compute_frame(rotation_A: float, rotation_B: float) -> np.ndarray:
    cos_A = np.cos(rotation_A)
    sin_A = np.sin(rotation_A)
    cos_B = np.cos(rotation_B)
    sin_B = np.sin(rotation_B)

    output = np.full((SCREEN_SIZE, SCREEN_SIZE), " ")
    zbuffer = np.zeros((SCREEN_SIZE, SCREEN_SIZE))

    cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, PHI_SPACING))
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, THETA_SPACING))
    sin_theta = np.sin(theta)
    circle_x = outer_radius + inner_radius * cos_theta
    circle_y = inner_radius * sin_theta

    x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T
    y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T
    z = ((projection_plane_distance + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T
    ooz = np.reciprocal(z)  # Calculates 1/z
    xp = (SCREEN_SIZE / 2 + projection_plane_scaling * ooz * x).astype(int)
    yp = (SCREEN_SIZE / 2 - projection_plane_scaling * ooz * y).astype(int)
    # Compute lighting effect
    L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta)
    L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A) * sin_B)
    L = np.around(((L1 + L2) * 8)).astype(int).T
    mask_L = L >= 0
    chars = ILLUMINATION_CHARS[L]

    for i in range(90):
        mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])
        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output



def pretty_print(frame: np.ndarray) -> None:
    for row in frame:
        colored_row = [map_char_to_color(char) + char for char in row]
        print(" ".join(colored_row) + TerminalColors.RESET)


if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('up'):
            inner_radius += ZOOM_SPEED
            outer_radius += ZOOM_SPEED
        elif keyboard.is_pressed('down'):
            inner_radius -= ZOOM_SPEED
            outer_radius -= ZOOM_SPEED

        rotation_A += THETA_SPACING
        rotation_B += PHI_SPACING
        print("\x1b[H")
        pretty_print(compute_frame(rotation_A, rotation_B))
        time.sleep(0.03)