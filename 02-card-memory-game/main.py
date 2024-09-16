from fasthtml.common import *
from fasthtml.svg import *
from svgs import fasthtml_logo
from fasthtml_hf import setup_hf_backup

app,rt = fast_app(
	live=True,
	id=int,
	title=str,
	done=bool,
	pk='id',
	hdrs=(Script(src="https://unpkg.com/alpinejs", defer=True), Link(rel="stylesheet", href="/public/app.css", type="text/css"),),
	pico=False,
    debug=True,
)

js = """
function game() {
    const cds = [];
    let id =  1;
    for (let i = 1; i <= 12; i++) {
        cds.push({ id: id++, flipped: false, cleared: false, card: i });
        cds.push({ id: id++, flipped: false, cleared: false, card: i });
    }
    cds.sort((a, b) => 0.5 - Math.random());
    
    return {
        card_clicks: 0,
        cheats: 3,
        cards: cds,
        get flippedCards() {
            return this.cards.filter(card => card.flipped);
        },
        flipCard(card) {
            this.card_clicks += 1;
            if( card.cleared ) { return; }
            if( this.flippedCards.length <= 1 ) { card.flipped = ! card.flipped; }
             
            if( this.flippedCards.length === 2 ) {
                if( this.flippedCards[0].card === this.flippedCards[1].card ) {
                    this.flippedCards.forEach(card => {
                        card.cleared = true;
                        card.flipped = false;
                    });
                } else {
                    if( card.id !== this.flippedCards[0].id && card.id !== this.flippedCards[1].id ) {
                        this.flippedCards.forEach(card => {
                            card.flipped = false;
                        });
                        card.flipped = ! card.flipped;
                    } else {
                        setTimeout((cd, fl) => {
                            fl.forEach(card => {
                                card.flipped = false;
                            });   
                        }, 1000, card, this.flippedCards);
                    }
                }
            }
        },
        restart() {
            this.cards.forEach(c => {
                c.flipped = false;
                c.cleared = false;
            });
            this.cheats = 3;
            this.card_clicks = 0;
            setTimeout(() => {
                this.cards.sort((a, b) => 0.5 - Math.random());   
            }, 500);
        },
        cheat() {
            if( this.cheats >= 1 ) {
                this.cheats -= 1;
                this.cards.forEach(c => {
                    c.flipped = true;
                });
                setTimeout(() => {
                    this.cards.forEach(c => {
                        c.flipped = false;
                    });
                }, 750);
            }
        },
    };
}
"""

def cards():
    return Template(
        Div(
            Div(
                Div(
                    NotStr(fasthtml_logo),
                    cls='flip-card-front'
                ),
                Div(
                    Img(
                        #src='/assets/card_imgs/' + card_num + '.png',
                        **{":src": "'/assets/card_imgs/' + card.card + '.png'"},
                    ),
                    cls='flip-card-back'
                ),
                cls='flip-card-inner',
                **{":class": "{'flip-rotate-y-180': card.flipped || card.cleared}"},
            ),
            tabindex='0',
            cls='flip-card',
            **{"@click": "flipCard(card)"},
            **{":class": "{'flip-cleared': card.cleared}"},
        ),
        x_for='card in cards',
        id="fr",
        data_something="123"
)

@rt('/')
def get(): return Title('Card Memory Game in FastHTML'), Div(
    Section(
        Div(
            H1('Card Memory Game', cls='text-4xl md:text-6xl font-bold mb-4'),
            P('Built with FastHTML, HTMX, TailwindCSS, and AlpineJS.', cls='text-lg md:text-2xl'),
            cls='text-center text-white px-6 md:px-12 drop-shadow-lg'
        ),
        cls='min-h-[300px] flex items-center justify-center bg-gradient-to-r from-[#3cdd8c] to-[#ffdb6d]'
    ),
	Section(
        Div(
            Div(
                Div(
                    cards(),
                    cls='grid grid-cols-6 gap-4 w-[944px]'
                ),
            ),
            cls='flex items-center justify-center mt-10'
        ),
        Div(
            Div(
                Div(),
                cls='flex items-center justify-center my-5 font-bold',
                **{"x-text": "'Card clicks: ' + card_clicks"},
            ),
            Div(
                A(
                    'Restart Game',
                    cls='bg-white text-[#3cdd8c] font-semibold px-6 py-3 rounded-lg shadow-lg hover:bg-gray-100 transition',
                    **{"x-on:click.prevent": "restart()"},
                ),
                A(
                    cls='bg-white text-[#3cdd8c] font-semibold px-6 py-3 rounded-lg shadow-lg hover:bg-gray-100 transition',
                    **{"x-on:click.prevent": "cheat()"},
                    **{"x-text": "'Cheat Mode! (' + cheats + ')'"},
                ),
                cls='flex items-center justify-center gap-4'
            ),
            Div(
                'Reveal all the matching pairs of cards in the fewest clicks possible.',
                cls='mt-6 flex items-center justify-center gap-4'
            ),
            Div(
                'Click the \'Cheat Mode\' button to reveal all tiles, but you only have three per game so use wisely!',
                cls='flex items-center justify-center gap-4'
            ),
        ),
        cls='mb-20',
        x_data='game()',
    ),
    Footer(
        A('Created by David Gwyer - Follow me on X', href="https://x.com/dgwyer", _target="_blank", cls="drop-shadow-lg text-lg"),
        cls='bg-gray-800 text-white text-center py-8'
    ),
    cls='bg-gray-100 text-gray-800'
), Script(js)

setup_hf_backup(app)

serve(reload_includes=["*.css"])
