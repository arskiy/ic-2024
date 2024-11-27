from manim import *


class Campo(ThreeDScene):
    def campo(self, t):
        return (0, 0, 0)

    def construct(self):
        k = ValueTracker(2)
        scl = ValueTracker(0.5)
        func = ParametricFunction(
            self.campo, t_range=(0, TAU), fill_opacity=0
        ).set_color(RED)
        func.add_updater(
            lambda m: m.become(
                ParametricFunction(
                    lambda t: (
                        scl.get_value() * np.cos(k.get_value() * t) * np.cos(t),
                        scl.get_value() * np.cos(k.get_value() * t) * np.sin(t),
                        scl.get_value() * -np.cos(2 * k.get_value() * t) * 0.5,
                    ),
                    t_range=(0, TAU),
                    fill_opacity=0,
                    color=RED,
                )
            )
        )

        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)

        self.add(func)
        self.play(scl.animate.set_value(3.5), run_time=2)
        self.move_camera(0, -60 * DEGREES, run_time=1)
        self.play(k.animate.set_value(4), run_time=2)
        self.wait()


class CampoPlano(Scene):
    def construct(self):
        func = lambda pos: np.array(
            [
                pos[0] ** 4 - 6 * pos[0] ** 2 * pos[1] ** 2 + pos[1] ** 4,
                4 * pos[0] ** 3 * pos[1] - 4 * pos[0] * pos[1] ** 3,
                0,
            ]
        )
        self.add(ArrowVectorField(func))


def proj_estereo_inv(pos):
    x = pos[0]
    y = pos[1]
    return np.array(
        [
            2 * x / (x**2 + y**2 + 1),
            2 * y / (x**2 + y**2 + 1),
            (x**2 + y**2 - 1) / (x**2 + y**2 + 1),
        ]
    )


def proj_estereo_inv_dif(pos):
    x = pos[0]
    y = pos[1]
    return np.array(
        [
            (2 * x * (y**2 - x**2 + 1) - 4 * x * y**2) / (x**2 + y**2 + 1) ** 2,
            (2 * y * (x**2 - y**2 + 1) - 4 * x**2 * y) / (x**2 + y**2 + 1) ** 2,
            (4 * x**2 + 4 * y**2) / (x**2 + y**2 + 1) ** 2,
        ]
    )


class SpawningAndFlowingArea(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)
        # func = lambda pos: x = pos[0], y = pos[1]; np.array([2*x/(x**2+y**2+1), 2*y/(x**2+y**2+1), (x**2+y**2-1)/(x**2+y**2+1)])
        stream_lines = StreamLines(
            proj_estereo_inv_dif,
            x_range=[-1, 1, 0.4],
            y_range=[-1, 1, 0.4],
            z_range=[-1, 1, 0.4],
            padding=1,
            virtual_time=1,
        )
        self.add(stream_lines)


class Pontryagin(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)
        for b in range(-10, 10):
            func = ParametricFunction(
                lambda t: proj_estereo_inv([t, t + float(b)/2]),
                t_range=(-TAU, TAU),
                fill_opacity=0,
                color=RED,
            )
            self.add(func)
        self.begin_ambient_camera_rotation(about="theta", rate=0.35)
        self.wait(3)

