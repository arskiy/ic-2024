from manim import *
import copy




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
                        scl.get_value() * -np.cos(2*k.get_value()*t) * 0.5,
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
