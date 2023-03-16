from typing import List
from urllib.parse import unquote

import flask
from py2html import HTMLElement
from py2html.ext import Script, Style
from py2html.elements import (a, body, button, div, h4, h5, head, hr, html,
                              iframe, image, input, span)

import iwashi

from .styles import (button_style, card_style, center_style, container_style,
                     copyright_style, frame_style, input_style, link_style,
                     links_style, margin_style, outline_style, style)

app = flask.Flask(__name__)


@app.route('/submit/<path:path>')
def submit(path: str) -> str:
    result = iwashi.visit(unquote(path))

    def condition(condition: bool, item: HTMLElement) -> List[HTMLElement]:
        return [item] if condition else []

    def card(result: iwashi.Result) -> HTMLElement:
        return div[
            outline_style(div[
                *condition(result.profile_picture, image(src=result.profile_picture, width='64', height='64')),
                div[
                    result.site_name
                ],
                *condition(result.url, div[
                    link_style(
                        a(href=result.url)[
                            result.url
                        ]
                    )
                ]),
                hr,
                *condition(result.title, div[
                    h5[
                        'name'
                    ],
                    span[
                        result.title
                    ]
                ]),
                *condition(result.description, div[
                    h5[
                        'description'
                    ],
                    span[
                        result.description
                    ]
                ]),
                *condition(
                    result.links,
                    div[
                        h5[
                            'links'
                        ],
                        *map(
                            lambda link: margin_style(h5[link_style(a(href=link)[link])]),
                            result.links
                        )
                    ]
                )
            ]),
            *condition(
                result.children,
                div[
                    links_style(h4[
                        'links'
                    ]),
                    card_style(div[
                        *map(
                            card,
                            result.children
                        )
                    ])
                ]
            )
        ]

    app = App()
    app.use_style(style)

    return app[
        container_style(
            div[
                card(result)
            ]
        )
    ].render()

class document: ...
def encodeURIComponent(s: str) -> str: ...

class App:
    def __init__(self) -> None:
        self.items = []
        self.head_items = []

    def use_style(self, style: Style = None) -> Style:
        style = style or Style()
        self.head_items.append(style)
        return style
    
    def use_script(self) -> Script:
        script = Script()
        self.head_items.append(script)
        return script

    def __getitem__(self, item) -> HTMLElement:
        if isinstance(item, tuple):
            items = item
        else:
            items = (item,)
        
        return html[
            head[
                *self.head_items
            ],
            body[
                *items
            ]
        ]
        
        

@app.route('/')
def index():
    app = App()
    app.use_style(style)
    script = app.use_script()

    @script
    def submit():
        url = document.getElementById('url_input').value
        frame = document.getElementById('frame')
        if frame:
            frame.src = f'/submit/{encodeURIComponent(url)}'

    @script
    def on_input_change(event):
        if event.keyCode == 13:
            submit()

    return app[
        center_style(body[
            div[
                input_style(input(id='url_input', type='text', onkeypress=on_input_change('event'))),
                button_style(button(onclick=submit)[
                    'Create'
                ])
            ]
        ]),
        frame_style(iframe(id='frame')),
        copyright_style(div[
            a(href='https://github.com/am230/iwashi')['Iwashi'],
            ' by ',
            a(href='https://github.com/am230/')['二時半'],
            ' with ',
            a(href='https://github.com/am230/py2html')['Py2HTML']
        ])
    ].render()


def run_server():
    app.run(host='0.0.0.0', port=5000)
