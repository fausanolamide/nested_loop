from manim import *
import numpy as np

# Configure vertical 9:16 resolution for YouTube Shorts / TikTok / Reels
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.background_color = "#121212"


class ExpressiveStickman(VGroup):
    """Articulated 2D stickman with laptop, fire hazard, and sunglasses."""
    def __init__(self, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        self.head = Circle(radius=0.34, color=color, stroke_width=6).move_to(UP * 1.2)
        self.body = Line(self.head.get_bottom(), DOWN * 0.25, color=color, stroke_width=6)

        init_shoulder = self.body.point_from_proportion(0.28)
        init_hip = self.body.get_end()

        self.left_arm = Line(init_shoulder, init_shoulder + LEFT * 0.55 + DOWN * 0.45, color=color, stroke_width=6)
        self.right_arm = Line(init_shoulder, init_shoulder + RIGHT * 0.55 + DOWN * 0.45, color=color, stroke_width=6)
        self.left_leg = Line(init_hip, init_hip + LEFT * 0.38 + DOWN * 1.1, color=color, stroke_width=6)
        self.right_leg = Line(init_hip, init_hip + RIGHT * 0.38 + DOWN * 1.1, color=color, stroke_width=6)

        # Laptop prop
        kb = Line(ORIGIN, RIGHT * 0.85, color="#78DCE8", stroke_width=7)
        scr = Line(RIGHT * 0.85, RIGHT * 1.12 + UP * 0.65, color="#78DCE8", stroke_width=7)
        self.laptop = VGroup(kb, scr).move_to(init_shoulder + RIGHT * 0.75 + DOWN * 0.28)

        # Laptop fire flames (hidden until O(n^2) meltdown)
        f1 = Polygon(ORIGIN, RIGHT * 0.25, UP * 0.55 + RIGHT * 0.12, fill_color="#FF6188", fill_opacity=1, stroke_width=0)
        f2 = Polygon(ORIGIN, RIGHT * 0.22, UP * 0.45 + RIGHT * 0.11, fill_color="#FFD866", fill_opacity=1, stroke_width=0).shift(RIGHT * 0.18)
        self.fire = VGroup(f1, f2).next_to(self.laptop, UP, buff=0.05).set_opacity(0)

        # Sunglasses prop (hidden until Senior enters)
        l_lens = RoundedRectangle(corner_radius=0.04, width=0.27, height=0.14, fill_color="#78DCE8", fill_opacity=1, stroke_width=0)
        r_lens = RoundedRectangle(corner_radius=0.04, width=0.27, height=0.14, fill_color="#78DCE8", fill_opacity=1, stroke_width=0)
        bridge = Line(LEFT * 0.16, RIGHT * 0.16, color="#78DCE8", stroke_width=4)
        l_lens.move_to(self.head.get_center() + LEFT * 0.14 + UP * 0.04)
        r_lens.move_to(self.head.get_center() + RIGHT * 0.14 + UP * 0.04)
        bridge.move_to(self.head.get_center() + UP * 0.04)
        self.glasses = VGroup(l_lens, r_lens, bridge).set_opacity(0)

        # Coffee mug (Senior prop)
        mug_body = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.38, fill_color="#E5C07B", fill_opacity=1, stroke_width=0)
        mug_handle = Circle(radius=0.12, color="#E5C07B", stroke_width=3).next_to(mug_body, RIGHT, buff=-0.05)
        self.coffee = VGroup(mug_body, mug_handle).next_to(self.left_arm.get_end(), DOWN, buff=-0.05).set_opacity(0)

        self.add(
            self.head, self.body,
            self.left_arm, self.right_arm,
            self.left_leg, self.right_leg,
            self.laptop, self.fire, self.glasses, self.coffee
        )

    @property
    def shoulder(self):
        """Dynamically computes the current shoulder position from the body Line."""
        return self.body.point_from_proportion(0.28)

    def typing_pose(self):
        kb = self.laptop[0].get_center()
        sh = self.shoulder
        return AnimationGroup(
            self.left_arm.animate.put_start_and_end_on(sh, kb + LEFT * 0.12 + UP * 0.08),
            self.right_arm.animate.put_start_and_end_on(sh, kb + RIGHT * 0.12 + UP * 0.14),
            run_time=0.25
        )

    def sip_coffee_pose(self):
        self.coffee.set_opacity(1)
        sh = self.shoulder
        return AnimationGroup(
            self.left_arm.animate.put_start_and_end_on(sh, self.head.get_center() + LEFT * 0.45 + DOWN * 0.1),
            self.coffee.animate.move_to(self.head.get_center() + LEFT * 0.45 + DOWN * 0.1),
            run_time=0.45
        )


def build_indented_code(data, font_size=21, line_spacing=0.44, left_margin=-3.0, top_y=3.4, space_w=0.145):
    """Explicitly positions each line taking indentation into account so spaces never collapse."""
    group = VGroup()
    for i, (indent_spaces, text_str, color) in enumerate(data):
        mob = Text(text_str, font="Consolas", font_size=font_size, color=color)
        target_left = left_margin + indent_spaces * space_w
        mob.move_to([target_left + mob.width / 2, top_y - i * line_spacing, 0])
        group.add(mob)
    return group


class NestedLoopEp5Short(Scene):
    def start_typing(self, stickman):
        """Scene-level updater for guaranteed real-time hand typing clatter at 60fps."""
        self.stop_typing(stickman)
        self._typing_t = 0.0

        def typing_updater(dt):
            self._typing_t += dt
            t = self._typing_t
            kb = stickman.laptop[0].get_center()
            sh = stickman.shoulder
            left_y = np.sin(t * 22) * 0.12 + 0.09
            right_y = np.cos(t * 22) * 0.12 + 0.09
            left_x = np.cos(t * 14) * 0.06 - 0.12
            right_x = np.sin(t * 16) * 0.06 + 0.12
            stickman.left_arm.put_start_and_end_on(sh, kb + RIGHT * left_x + UP * left_y)
            stickman.right_arm.put_start_and_end_on(sh, kb + RIGHT * right_x + UP * right_y)

        self._current_typing_updater = typing_updater
        self.add_updater(typing_updater)

    def stop_typing(self, stickman):
        """Removes the scene updater and settles hands cleanly on the laptop."""
        if hasattr(self, "_current_typing_updater") and self._current_typing_updater is not None:
            self.remove_updater(self._current_typing_updater)
            self._current_typing_updater = None
        kb = stickman.laptop[0].get_center()
        sh = stickman.shoulder
        stickman.left_arm.put_start_and_end_on(sh, kb + LEFT * 0.12 + UP * 0.08)
        stickman.right_arm.put_start_and_end_on(sh, kb + RIGHT * 0.12 + UP * 0.14)

    def construct(self):
        # =========================================================
        # FRAME 0: SERIES BADGE + HOOK + STICKMAN (Universal Safe-Zone)
        # =========================================================
        ep_pill_bg = RoundedRectangle(
            corner_radius=0.14, width=3.4, height=0.42,
            fill_color="#252526", fill_opacity=1, stroke_color="#FFD866", stroke_width=1.5
        ).move_to(UP * 5.78)
        ep_pill_txt = Text("DEV PAIN • EP. 05", font_size=19, color="#FFD866", weight=BOLD).move_to(ep_pill_bg)
        ep_badge = VGroup(ep_pill_bg, ep_pill_txt)

        meme_card = RoundedRectangle(
            corner_radius=0.18, width=6.6, height=1.08,
            fill_color="#1E1E1E", fill_opacity=1, stroke_color="#FFD866", stroke_width=3
        ).move_to(UP * 4.72)
        cap_top = Text('"Works fine on my laptop"', font_size=23, color="#FFD866", weight=BOLD)
        if cap_top.width > 6.0:
            cap_top.scale_to_fit_width(6.0)
        cap_bot = Text("Until production has 100,000 rows:", font_size=18, color=WHITE)
        if cap_bot.width > 6.0:
            cap_bot.scale_to_fit_width(6.0)
        meme_header = VGroup(meme_card, VGroup(cap_top, cap_bot).arrange(DOWN, buff=0.08).move_to(meme_card))

        stickman = ExpressiveStickman().scale(0.68).move_to(DOWN * 3.35 + LEFT * 0.25)

        self.add(ep_badge, meme_header, stickman)
        stickman.save_state()

        # =========================================================
        # ACT 1: NESTED LOOP WORKS ON 10 ITEMS (0:01 - 0:11)
        # =========================================================
        self.play(stickman.typing_pose(), run_time=0.35)
        self.start_typing(stickman)

        code_data = [
            (0, "for x in users:", "#78DCE8"),
            (4, "if x in banned_list:", "#FFD866"),
            (8, "block(x)", WHITE),
        ]
        code_lines = build_indented_code(code_data, font_size=22, line_spacing=0.44, left_margin=-2.8, top_y=3.45)
        if code_lines.width > 6.4:
            code_lines.scale_to_fit_width(6.4)

        for line in code_lines:
            self.play(AddTextLetterByLetter(line), run_time=0.75)
            self.wait(0.1)
        self.stop_typing(stickman)

        test_badge = RoundedRectangle(
            corner_radius=0.16, width=6.5, height=0.76,
            fill_color="#A9DC76", fill_opacity=0.22, stroke_color="#A9DC76", stroke_width=2
        ).move_to(UP * 1.45)
        test_txt = Text("Test (N = 10): 0.001s  ->  Ship it!", font="Consolas", font_size=20, color="#A9DC76", weight=BOLD).move_to(test_badge)
        if test_txt.width > 6.0:
            test_txt.scale_to_fit_width(6.0)
        test_group = VGroup(test_badge, test_txt)

        self.play(FadeIn(test_group, scale=0.9), run_time=0.45)
        self.wait(2.2)

        # =========================================================
        # ACT 2: PROD 100,000 ROWS -> O(n^2) MELTDOWN (0:11 - 0:22)
        # =========================================================
        self.play(FadeOut(test_group), run_time=0.25)

        prod_banner = RoundedRectangle(
            corner_radius=0.18, width=6.6, height=1.35,
            fill_color="#FF6188", fill_opacity=0.24, stroke_color="#FF6188", stroke_width=3
        ).move_to(UP * 1.15)
        p_t1 = Text("PROD: N = 100,000  ->  O(n^2)", font="Consolas", font_size=22, color="#FF6188", weight=BOLD)
        p_t2 = Text("10,000,000,000 checks | CPU 99°C", font="Consolas", font_size=19, color=WHITE, weight=BOLD)
        prod_content = VGroup(p_t1, p_t2).arrange(DOWN, buff=0.12).move_to(prod_banner)
        if prod_content.width > 6.1:
            prod_content.scale_to_fit_width(6.1)
        prod_group = VGroup(prod_banner, prod_content)

        # Laptop catches fire and stickman topples backward!
        self.play(
            FadeIn(prod_group, scale=0.85),
            stickman.fire.animate.set_opacity(1),
            stickman.laptop.animate.set_color("#FF6188"),
            stickman.animate.set_color("#FF6188"),
            run_time=0.55
        )
        # Flames flicker while stickman faints
        self.play(
            stickman.fire.animate.scale(1.25),
            stickman.animate.rotate(0.45).shift(DOWN * 0.2),
            run_time=0.55
        )
        self.play(stickman.fire.animate.scale(0.85), run_time=0.35)
        self.wait(3.2)

        # Clear Act 1 & 2
        self.play(
            FadeOut(VGroup(code_lines, prod_group), shift=LEFT * 2),
            stickman.animate.shift(LEFT * 6),
            run_time=0.6
        )

        # =========================================================
        # ACT 3: SENIOR DEV O(1) SET() FIX (0:22 - 0:33)
        # =========================================================
        stickman.restore()
        stickman.fire.set_opacity(0)
        stickman.move_to(DOWN * 3.35 + RIGHT * 6)
        stickman.glasses.set_opacity(1)
        stickman.coffee.set_opacity(1)

        sr_tag = Text("SENIOR DEV (Hash Set = O(1)):", font="Consolas", font_size=22, color="#A9DC76", weight=BOLD).move_to(UP * 3.75)
        if sr_tag.width > 6.4:
            sr_tag.scale_to_fit_width(6.4)
        self.play(
            FadeIn(sr_tag, shift=DOWN * 0.2),
            stickman.animate.move_to(DOWN * 3.35 + LEFT * 0.25),
            run_time=0.75
        )
        self.play(stickman.typing_pose(), run_time=0.25)
        self.start_typing(stickman)

        sr_data = [
            (0, "banned_set = set(banned_list)", "#A9DC76"),
            (0, "for x in users:", "#78DCE8"),
            (4, "if x in banned_set:", "#FFD866"),
            (8, "block(x)", WHITE),
        ]
        sr_lines = build_indented_code(sr_data, font_size=21, line_spacing=0.40, left_margin=-2.9, top_y=3.00)
        if sr_lines.width > 6.4:
            sr_lines.scale_to_fit_width(6.4)

        for line in sr_lines:
            self.play(AddTextLetterByLetter(line), run_time=0.65)
        self.stop_typing(stickman)

        ok_box = RoundedRectangle(
            corner_radius=0.18, width=6.6, height=1.20,
            fill_color="#A9DC76", fill_opacity=0.22, stroke_color="#A9DC76", stroke_width=3
        ).move_to(UP * 0.70)
        ok_title = Text(">>> PROD: 0.02s  (O(n))", font="Consolas", font_size=22, color="#A9DC76", weight=BOLD)
        ok_sub = Text("100,000 checks | CPU 4%!", font="Consolas", font_size=19, color=WHITE)
        ok_content = VGroup(ok_title, ok_sub).arrange(DOWN, buff=0.10).move_to(ok_box)
        if ok_content.width > 6.1:
            ok_content.scale_to_fit_width(6.1)
        ok_group = VGroup(ok_box, ok_content)

        self.play(
            FadeIn(ok_group, shift=UP * 0.35),
            stickman.sip_coffee_pose(),
            run_time=0.45
        )
        self.wait(2.6)

        # =========================================================
        # CLEAR SCREEN END CARD: STICKMAN + FOLLOW CTA CENTERED
        # =========================================================
        cta_txt = Text("Follow for Ep. 6", font="Consolas", font_size=26, color="#78DCE8", weight=BOLD)
        cta_box = RoundedRectangle(
            corner_radius=0.22, width=cta_txt.width + 1.1, height=0.80,
            fill_color="#1E1E1E", fill_opacity=0.98, stroke_color="#78DCE8", stroke_width=2.5
        ).move_to(UP * 0.8)
        cta_txt.move_to(cta_box)
        cta_pill = VGroup(cta_box, cta_txt)

        self.play(
            FadeOut(VGroup(sr_tag, sr_lines, ok_group, meme_header), shift=UP * 0.3),
            stickman.animate.move_to(DOWN * 1.2 + LEFT * 0.2),
            FadeIn(cta_pill, scale=0.9),
            run_time=0.45
        )
        self.wait(1.6)

        # =========================================================
        # SEAMLESS LOOP RESET (Matches Frame 0 Identically)
        # =========================================================
        stickman.glasses.set_opacity(0)
        stickman.coffee.set_opacity(0)
        self.play(
            FadeOut(cta_pill, scale=0.9),
            FadeIn(meme_header),
            Restore(stickman),
            run_time=0.55
        )
        self.wait(0.2)
