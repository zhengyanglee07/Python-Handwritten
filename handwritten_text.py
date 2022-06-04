from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.request import Request

from PIL import Image, ImageFont
from handright import Template, handwrite


def generateHandwrittenText(text):
    font_file_name = 'fonts/Bo Le Locust Tree Handwriting Pen Chinese Font-Simplified Chinese Fonts.ttf'

    template = Template(
        background=Image.new(mode="1", size=(1024, 2048), color=1),
        font=ImageFont.truetype(font_file_name, size=100),
    )

    images = handwrite(text, template)
    imgList = []
    for i, im in enumerate(images):
        assert isinstance(im, Image.Image)
        im.show()
        file_name = "static/images/text-{}.webp".format(i)
        im.save(file_name)
        imgList.append(file_name)

    return imgList


@view_config(route_name="generate", renderer="json")
def generate(request: Request):
    imgList = generateHandwrittenText(request.text)
    return {"imgList": imgList, "text": request.text}


@view_config(
    route_name="home",
    renderer="templates/index.jinja2"
)
def home(request):
    return {}


if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.add_static_view(name='static', path='static')
        config.include('pyramid_debugtoolbar')

        config.add_route('home', '/')
        config.add_route('generate', '/generate')

        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
