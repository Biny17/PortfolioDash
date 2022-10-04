import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

header = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand("Title", className="ms-2")),
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Home")),
                                dbc.NavItem(dbc.NavLink("Page 1")),
                                dbc.NavItem(
                                    dbc.NavLink("Page 2"),
                                    # add an auto margin after page 2 to
                                    # push later links to end of nav
                                    className="me-auto",
                                ),
                                dbc.NavItem(dbc.NavLink("Help")),
                                dbc.NavItem(dbc.NavLink("About")),
                            ],
                            # make sure nav takes up the full width for auto
                            # margin to get applied
                            className="w-100",
                        ),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                # the row should expand to fill the available horizontal space
                className="flex-grow-1",
            ),
        ],
        fluid=True,
    ),
    dark=True,
    color="dark",
)

app.layout = html.Div(
    [header, dbc.Container(html.P("This is some content"), className="p-5")]
)

if __name__ == "__main__":
    app.run_server(debug=True)