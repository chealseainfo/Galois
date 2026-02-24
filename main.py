from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from math import sqrt, acos, cos, pi


# ---------- Polynomial Utilities ----------

def quadratic_roots(a, b, c):
    disc = b * b - 4 * a * c
    r1 = (-b + sqrt(disc)) / (2 * a)
    r2 = (-b - sqrt(disc)) / (2 * a)
    return [r1, r2], disc


def cubic_roots(a, b, c, d):
    # Depressed cubic: x^3 + px + q = 0
    p = (3 * a * c - b * b) / (3 * a * a)
    q = (2 * b ** 3 - 9 * a * b * c + 27 * a * a * d) / (27 * a * a * a)
    disc = (q / 2) ** 2 + (p / 3) ** 3
    roots = []
    if disc > 0:
        # One real root, two complex
        A = (-q / 2 + disc ** 0.5) ** (1 / 3)
        B = (-q / 2 - disc ** 0.5) ** (1 / 3)
        x1 = A + B - b / (3 * a)
        x2 = -(A + B) / 2 - b / (3 * a) + (A - B) * (3 ** 0.5) / 2 * 1j
        x3 = -(A + B) / 2 - b / (3 * a) - (A - B) * (3 ** 0.5) / 2 * 1j
        roots = [x1, x2, x3]
    else:
        # Three real roots
        r = 2 * sqrt(-p / 3)
        theta = acos(3 * q / (2 * p) * sqrt(-3 / p))
        x1 = r * cos(theta / 3) - b / (3 * a)
        x2 = r * cos((theta + 2 * pi) / 3) - b / (3 * a)
        x3 = r * cos((theta + 4 * pi) / 3) - b / (3 * a)
        roots = [x1, x2, x3]
    return roots, disc


def guess_galois_group(degree, disc):
    if degree == 2:
        return "C2 (order 2)"
    if degree == 3:
        return "A3 (Δ>0) or S3 (Δ<0)"
    return "Not supported"


# ---------- Screens ----------

class First(Screen):
    pass


class GaloisCalculator(Screen):
    def compute_galois(self):
        try:
            text = self.ids.coeff_input.text
            coeffs = [float(c.strip()) for c in text.split(",")]
            degree = len(coeffs) - 1
            self.ids.degree_output.text = str(degree)

            if degree == 2:
                roots, disc = quadratic_roots(*coeffs)
            elif degree == 3:
                roots, disc = cubic_roots(*coeffs)
            else:
                self.ids.disc_output.text = ""
                self.ids.roots_output.text = "Only quadratics and cubics supported"
                self.ids.group_output.text = ""
                return

            self.ids.disc_output.text = str(disc)
            self.ids.roots_output.text = "\n".join([str(r) for r in roots])
            self.ids.group_output.text = guess_galois_group(degree, disc)
        except Exception as e:
            self.ids.roots_output.text = f"Error: {e}"
            self.ids.disc_output.text = ""
            self.ids.group_output.text = ""
            self.ids.degree_output.text = ""

    def clear_fields(self):
        self.ids.coeff_input.text = ""
        self.ids.degree_output.text = ""
        self.ids.disc_output.text = ""
        self.ids.roots_output.text = ""
        self.ids.group_output.text = ""


# ---------- App ----------

class GaloisApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(First(name="first"))
        sm.add_widget(GaloisCalculator(name="calculator"))
        return sm


if __name__ == "__main__":
    GaloisApp().run()