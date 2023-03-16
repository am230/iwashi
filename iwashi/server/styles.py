from py2html.ext import Style

style = Style()

accent = style.define('#3da0b4')

style.style('hr', {
    'color': accent,
})

card_style = style({
    'background-color': '#fff',
    'height': '50px',
    'width': '200px',
    'height': 'auto',
    'box-shadow': f'-1px 0px 0px 0px {accent}',
    'padding-left': '40px',
    'margin': '10px'
})

link_style = style({
    'margin': '0px'
})

outline_style = style({
    'padding': '10px',
    'margin': '10px',
    'width': 'min-content',
    'border': f'1px solid {accent}',
    'box-shadow': f'-4px 0px 0px 0px {accent}'
})

links_style = style({
    'padding-left': '10px'
})

margin_style = style({
    'margin': '0px'
})

container_style = style({
    'display': 'flex',
    'justify-content': 'center'
})

center_style = style({
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'flex-direction': 'column'
})

button_style = style({
    'outline': 'none',
    'border': f'1px solid {accent}',
    'background-color': accent,
    'width': '100px',
    'height': '40px',
    'color': '#fff',
    'font-size': '16px'
})


input_style = button_style | style({
    'background-color': '#fff',
    'width': '300px',
    'color': '#000',
    'padding-left': '10px'
})

frame_style = style({
    'margin-top': '5px',
    'width': '100%',
    'height': 'calc(100vh - 80px)',
    'border': 'none',
    'border-top': f'1px solid {accent}',
    'border-bottom': f'1px solid {accent}'
})

copyright_style = style({
    'font-size': '10px',
    'color': accent
})

style.style('*', {
    'font-family': 'sans-serif'
})

style.style('*::-webkit-scrollbar', {
    'width': '5px'
})

style.style('*::-webkit-scrollbar-track', {
    'background': '#fff'
})

style.style('*::-webkit-scrollbar-thumb', {
    'background': accent
})

style.style('a', {
    'color': accent,
    'text-underline-offset': '5px'
})
