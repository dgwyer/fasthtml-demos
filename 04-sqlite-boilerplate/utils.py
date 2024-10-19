from fasthtml.common import *

# Status code 303 is a redirect that can change POST to GET, so it's appropriate for a login page.
login_redir = RedirectResponse('/login', status_code=303)
home_redir = RedirectResponse('/', status_code=303)

@dataclass
class Login: name:str; pwd:str

def n_words(text, n):
    if not text: return ''
    words = text.split()
    if len(words) <= n:
        return text
    trimmed_text = ' '.join(words[:n])
    return NotStr(trimmed_text + '&hellip;')
