from fasthtml.common import *

# Custom 404 response
def _404(req, exc): return Title('404 - Page not found!'), Main(
    Div(
        P('404', cls='text-lg font-semibold text-indigo-600'),
        H1('Page not found', cls='mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl'),
        P('Sorry, we couldn’t find the page you’re looking for.', cls='mt-6 text-base leading-7 text-gray-600'),
        Div(
            Button(home_svg(), A('Home', href='/'), cls='btn'),
            cls='mt-10 flex items-center justify-center gap-x-6'
        ),
        cls='text-center'
    ),
    cls='grid min-h-full place-items-center bg-white px-6 py-24 sm:py-32 lg:px-8'
)

def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

def header(logo='assets/logo.svg', logo_alt='Made with FastHTML', links={}): return Div(
    Nav(
        Ul(
            Li(
                A(
                    Img(src=logo, alt=logo_alt, cls='w-[125px] h-[24px]'),
                    href='/'
                ),
				cls="mr-auto"
            ),
            *[Li(A(link, href=href)) for link, href in links.items()],
            cls="m-0 p-0 list-none flex flex-row flex-wrap gap-x-8 gap-y-4 justify-between items-end font-medium"
        ),
        cls="container-section"
    ),
)

def footer(logo='assets/logo.svg', logo_alt='Made with FastHTML', links={}): return Div(
    Nav(
        Ul(
            *[Li(A(link, href=href)) for link, href in links.items()],
            Li(
				Span('Built with'),
                A(
                    Img(src=logo, alt=logo_alt, cls='w-[125px] h-[24px] inline'),
                    href='https://www.fastht.ml/'
                ),
				cls="ml-auto"
            ),
            cls="m-0 p-0 list-none flex flex-row flex-wrap gap-x-8 gap-y-4 justify-between items-end font-medium"
        ),
        cls="container-section"
    ),
)

def home_svg(): return NotStr('<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="-ml-0.5 h-5 w-5"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>')
