#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_generation import *
from write_to_file import *
from plot_results import *
from TOPSIS.old_topsis import *
from UTA_BIS.UTA_STAR import *
from RSM.RSM_old import *

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
import time

from typing import List, Tuple

POINT = List[float]
POINTS = List[POINT]

DISTRIBUTIONS = ["Gaussa", "Eksponencjalny", "Beta", "Gamma", "Jednostajny"]
ALGORITHMS = ["TOPSIS", "UTA", "RSM"]

Builder.load_file("layout.kv")


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.points: POINTS = []
        self.points_labels: List[Label] = []
        self.not_dominated_points: POINTS = []
        self.point_counter: int = 0
        self.criteria_labels: List[Label] = []
        self.criteria_inputs: List[TextInput] = []
        self.criteria_buttons: List[ToggleButton] = []
        self.criteria_buttons_removal: List[Button] = []
        self.criteria_checkboxes: List[CheckBox] = []
        self.criteria_references1: List[TextInput] = []
        self.criteria_references2: List[TextInput] = []
        self.criteria_weights: List[TextInput] = []
        self.distribution_checkboxes: List[CheckBox] = []
        self.algorithm_checkboxes: List[CheckBox] = []
        self.point_labels: List[Label] = []
        self.dropdown_buttons: List[Button] = []
        self.points_removal = []

        box1 = self.ids["choose_distribution_1"]
        box2 = self.ids["choose_distribution_2"]

        for text in DISTRIBUTIONS:
            box1.add_widget(Label(text=text, color="black"))
            checkbox = CheckBox(group="distribution", color="black")
            box2.add_widget(checkbox)
            self.distribution_checkboxes.append(checkbox)

        box1 = self.ids["choose_algorithm_1"]
        box2 = self.ids["choose_algorithm_2"]

        for text in ALGORITHMS:
            box1.add_widget(Label(text=text, color="black"))
            checkbox = CheckBox(group="algorithm", color="black")
            box2.add_widget(checkbox)
            self.algorithm_checkboxes.append(checkbox)

    def add_criteria(self) -> None:
        box = self.ids["criteria_layout"]
        box.rows += 1
        criteria_counter = len(self.criteria_labels) + 1

        lbl = Label(text=str(criteria_counter), color="black")
        box.add_widget(lbl)
        self.criteria_labels.append(lbl)

        inp = TextInput(hint_text=f"Kryterium {criteria_counter}")
        box.add_widget(inp)
        self.criteria_inputs.append(inp)

        btn = ToggleButton(text="Min", on_press=lambda btn_: self.change_objective(btn_))
        box.add_widget(btn)
        self.criteria_buttons.append(btn)

        btn = Button(text="Usuń", on_press=lambda btn_, idx=criteria_counter - 1: self.remove_criteria(idx))
        box.add_widget(btn)
        self.criteria_buttons_removal.append(btn)

        checkbox = CheckBox(group="criteria", color="black")
        box.add_widget(checkbox)
        self.criteria_checkboxes.append(checkbox)

        inp = TextInput()
        box.add_widget(inp)
        self.criteria_references1.append(inp)

        inp = TextInput()
        box.add_widget(inp)
        self.criteria_references2.append(inp)

        inp = TextInput()
        box.add_widget(inp)
        self.criteria_weights.append(inp)

        box = self.ids["points_header_layout"]
        box.cols += 1

        lbl = Label(text=f"Kryterium {criteria_counter}", color="black")
        box.add_widget(lbl)
        self.point_labels.append(lbl)

        box = self.ids["points_layout"]
        box.cols += 1

    def remove_criteria(self, idx: int) -> None:
        box = self.ids["criteria_layout"]
        box.remove_widget(self.criteria_labels[idx])
        self.criteria_labels.pop(idx)
        box.remove_widget(self.criteria_inputs[idx])
        self.criteria_inputs.pop(idx)
        box.remove_widget(self.criteria_buttons[idx])
        self.criteria_buttons.pop(idx)
        box.remove_widget(self.criteria_buttons_removal[idx])
        self.criteria_buttons_removal.pop(idx)
        box.remove_widget(self.criteria_checkboxes[idx])
        self.criteria_checkboxes.pop(idx)
        box.remove_widget(self.criteria_references1[idx])
        self.criteria_references1.pop(idx)
        box.remove_widget(self.criteria_references2[idx])
        self.criteria_references2.pop(idx)
        box.remove_widget(self.criteria_weights[idx])
        self.criteria_weights.pop(idx)

        box = self.ids["points_header_layout"]
        box.remove_widget(self.point_labels[idx])
        self.point_labels.pop(idx)
        box.cols -= 1

        box = self.ids["points_layout"]
        box.cols -= 1

    def sort_points(self) -> None:
        for i, checkbox in enumerate(self.criteria_checkboxes):
            if checkbox.active:
                self.points = sorted(self.points, key=lambda v: v[i])
                break

        i = 0

        for point in self.points:
            for coord in point:
                self.points_labels[i].text = str(coord)
                i += 1

    def change_objective(self, btn: ToggleButton) -> None:
        btn.text = "Max" if btn.text == "Min" else "Min"

    def add_point(self):
        pass

    def generate_points(self):
        ids = ["par1", "par2", "n_points"]

        for id_ in ids:
            if self.ids[id_].text == "":
                return None

        par1 = float(self.ids["par1"].text)
        par2 = float(self.ids["par2"].text)
        number_of_points = int(self.ids["n_points"].text)
        number_of_parameters = len(self.criteria_inputs)
        distribution = None

        for i, checkbox in enumerate(self.distribution_checkboxes):
            if checkbox.active:
                distribution = i
                break

        if distribution is None:
            return None

        points: POINTS = []

        if distribution == 0:
            mean = par1
            std = par2
            points = generate_points_gaussian(mean, std, number_of_points, number_of_parameters)

        elif distribution == 1:
            scale = par2
            points = generate_points_exponential(scale, number_of_points, number_of_parameters)

        elif distribution == 2:
            a = par1
            b = par2
            points = generate_points_beta(a, b, number_of_points, number_of_parameters)

        elif distribution == 3:
            shape = par1
            scale = par2
            points = generate_points_gamma(shape, scale, number_of_points, number_of_parameters)

        elif distribution == 4:
            low = par1
            high = par2
            points = generate_points_uniform(low, high, number_of_points, number_of_parameters)

        points = list(map(tuple, points))

        self.points.extend(points)
        box = self.ids["points_layout"]

        for point in self.points:
            box.rows += 1

            for coord in point:
                lbl = Label(text=str(coord), color="black")
                box.add_widget(lbl)
                self.points_labels.append(lbl)

    def solve(self):
        algorithm = None

        for i, checkbox in enumerate(self.algorithm_checkboxes):
            if checkbox.active:
                algorithm = i
                break

        if algorithm is None:
            return None

        criteria = [btn.text == "Max" for btn in self.criteria_buttons]
        directions = [btn.text.lower() for btn in self.criteria_buttons]

        t1 = time.time()

        if algorithm == 0:
            reference = [[float(ref1.text), float(ref2.text)] for ref1, ref2 in zip(self.criteria_references1, self.criteria_references2)]
            weights = [float(w.text) for w in self.criteria_weights]
            rank = topsis(deepcopy(self.points), reference, weights)
            self.rank_points = [p[0] for p in rank[:3]]

        elif algorithm == 1:
            points = np.array([list(self.points[i]) for i in range(len(self.points))])
            rank = UTASTAR(points, criteria)[:3]
            self.rank_points = [self.points[idx] for idx in rank]

        elif algorithm == 2:
            points = np.array([list(self.points[i]) for i in range(len(self.points))])
            pref = np.array([1, 1, 1])
            pref_qwo = np.array([10, 10, 10])
            rank = determine_sets(pref, pref_qwo, points, directions)[:3, :]
            self.rank_points = [p for p in rank]

        t2 = time.time()
        print(f"Czas: {(t2 - t1) * 1000} [ms]")
        print(self.rank_points)

    def render_animation(self):
        plot_results(self.points, self.rank_points)

    def write_to_file(self):
        parameters: List[Tuple[str, str]] = []

        for i in range(len(self.criteria_inputs)):
            inp = self.criteria_inputs[i]
            btn = self.criteria_buttons[i]
            parameters.append((inp.hint_text, btn.text))

        write_results_to_file(self.points, self.not_dominated_points, parameters)


class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))

        return sm


if __name__ == "__main__":
    TestApp().run()