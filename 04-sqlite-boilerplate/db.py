from fasthtml.common import *
from utils import login_redir, n_words
from datetime import datetime

db = database('data/main.db')

todos,users = db.t.todos,db.t.users
if todos not in db.t:
    users.create(dict(id=int, name=str, pwd=str), pk='id')
    todos.create(id=int, title=str, done=bool, user_id=int, details=str, date=str, priority=int, pk='id')
Todo,User = todos.dataclass(),users.dataclass()

# Beforeware cb function, run before a route handler is called.
def before(req, sess):
    global todos
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth:
        sess['intended_url'] = req.url.path
        return login_redir
    todos.xtra(user_id=auth)

# The `patch` decorator, which is defined in `fastcore`, adds a method to an existing class.
# Here we are adding a method to the `Todo` class, which is returned by the `todos` table.
# The `__ft__` method is a special method that FastHTML uses to convert the object into an `FT` object,
# so that it can be composed into an FT tree, and later rendered into HTML.
@patch
def __ft__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', 'current-todo')
    edit = AX('Edit',     f'/edit/{self.id}' , 'current-todo', cls='text-indigo-600 hover:text-indigo-900')
    dt = '✅ ' if self.done else '❌'
    timestamp = int(self.date)
    formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    return Tr(
        Td(show, title="Display todo details", cls='py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-0'),
        Td(n_words(self.details, 5), cls='px-3 py-4 text-sm text-gray-500'),
        Td(dt, cls='px-3 py-4 text-sm text-gray-500'),
        Td(formatted_date, cls='px-3 py-4 text-sm text-gray-500'),
		Td(
			edit,
			cls='relative py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0'
		),
        id=f'todo-{self.id}'
	),
