from fasthtml.common import *

app,rt = fast_app(
	live=True,
	id=int,
	title=str,
	done=bool,
	pk='id',
	hdrs=(Link(rel="stylesheet", href="/public/app.css", type="text/css"),),
	pico=False,
)

@rt('/')
def get(): return Title('TailwindCSS in FastHTML'), Div(
    Section(
        Div(
            H1('TailwindCSS in FastHTML!', cls='text-4xl md:text-6xl font-bold mb-4'),
            P('And with live reload enabled, this is a great dev experience.', cls='text-lg md:text-2xl mb-8'),
            A('Get Started', href='#', cls='bg-white text-blue-500 font-semibold px-6 py-3 rounded-lg shadow-lg hover:bg-gray-100 transition'),
            cls='text-center text-white px-6 md:px-12'
        ),
        cls='min-h-[500px] flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600'
    ),
    Section(
        Div(
            Div(
                H2('Our Features', cls='text-3xl font-bold'),
                P('Discover what makes us the best in the business.', cls='text-gray-600'),
                cls='text-center mb-12'
            ),
            Div(
                Div(
                    H3('Feature One', cls='text-xl font-semibold mb-4'),
                    P('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', cls='text-gray-600'),
                    cls='bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition'
                ),
                Div(
                    H3('Feature Two', cls='text-xl font-semibold mb-4'),
                    P('Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', cls='text-gray-600'),
                    cls='bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition'
                ),
                Div(
                    H3('Feature Three', cls='text-xl font-semibold mb-4'),
                    P('Ut enim ad minim veniam, quis nostrud exercitation ullamco.', cls='text-gray-600'),
                    cls='bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition'
                ),
                cls='grid grid-cols-1 md:grid-cols-3 gap-8'
            ),
            cls='max-w-6xl mx-auto px-6'
        ),
        cls='pt-20 pb-24'
    ),
    Footer(
        P('© 2024 Your Company. All rights reserved.'),
        cls='bg-gray-800 text-white text-center py-6'
    ),
    cls='bg-gray-100 text-gray-800'
)

serve()