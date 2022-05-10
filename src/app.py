import PySimpleGUI as sg

from .scrapper import KayakScrapper

sg.theme('SandyBeach')


class TrackerApp:
    """GUI for the Kayak scrapper"""

    def __init__(self, timeout=20):
        self.timeout = timeout

    def _get_input_layout(self):
        """
        Layout of the GUI containing all input data.
        In the combo box, you can add any city you want.
        """
        input_layout = [
            [sg.Text('Departure Airport', size=(20, 1)),
             sg.Combo(["Strasbourg", "Paris", "Baden-Baden", "Mulhouse"], default_value="Strasbourg", key='from_city')],

            [sg.Text('Departure date', size=(20, 1)),
             sg.Input(key='departure_date', size=(20, 1)),
             sg.CalendarButton('Calendar', close_when_date_chosen=True, format='%d/%m/%Y', target='departure_date',
                               no_titlebar=False)],

            [sg.Text('Arrival date', size=(20, 1)),
             sg.Input(key='arrival_date', size=(20, 1)),
             sg.CalendarButton('Calendar', close_when_date_chosen=True, format='%d/%m/%Y', target='arrival_date',
                               no_titlebar=False)],

            [sg.Text('Maximum price', size=(20, 1)),
             sg.Slider((0, 500), key="max_price", orientation="h")],

            [sg.Submit(), sg.Cancel()]
        ]

        return input_layout

    def _get_output_layout(self):
        """Layout of the GUI containing all input data"""
        output_layout = [
            [sg.Text("You can go to :")],
            [sg.Text(sg.InputText(""), key='results', visible=False)]
        ]
        return output_layout

    def _get_layout(self, input_layout, output_layout):
        """All layout of the GUI"""
        layout = [
            [sg.Column(input_layout),
             sg.VSeperator(),
             sg.Column(output_layout)]
        ]
        return layout

    def run(self):
        """Run the application until the user quit the interface"""
        input_layout = self._get_input_layout()
        output_layout = self._get_output_layout()
        layout = self._get_layout(input_layout, output_layout)
        window = sg.Window('Need fresh air ?!', layout)

        while True:
            event, cfg = window.read()
            if event in ["Cancel", sg.WIN_CLOSED]:
                break
            else:
                scrapper = KayakScrapper(cfg, self.timeout)
                possible_trips = scrapper.scrape()
                possible_trips = {k: possible_trips[k]
                                  for k in list(possible_trips.keys())[:10]}
                trips_string = "\n".join(
                    f"- {k} for {v} euros" for k, v in possible_trips.items())
                window['results'].Update(trips_string, visible=True)

        window.close()
