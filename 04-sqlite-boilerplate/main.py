from fasthtml.common import *
from hmac import compare_digest
from templates import _404, clr_details, header, footer
from utils import login_redir, home_redir, Login
from db import before, todos, users, Todo, User
import subprocess

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/assets/.*', r'.*\.css', '/', '/login'])
app = FastHTMLWithLiveReload(before=bware,
               exception_handlers={404: _404},
               pico=False,
               hdrs=(
                     Link(rel="stylesheet", href="/public/app.css", type="text/css"),
                     )
                )
rt = app.route

### Homepage Routes ###

def header_html(sess):
    links = {'ToDos': '/todos', 'About': '/about', 'Contact': '/contact'}

    # Get the authenticated user from the session
    auth = sess.get('auth')
    if auth:
        user_info = H2(f"Welcome, {auth}!", cls="user-info")
        links['Logout'] = '/logout'
        
    else:
        user_info = H2("Welcome, Guest!", cls="user-info")
        links['Login'] = '/login'

    return (user_info, links)

@rt("/")
def get(sess):
    user_info, links = header_html(sess)

    return (
        header(links=links),
        Div(
            user_info,
            Div('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ut consequat neque, vel luctus elit. Nunc elementum sapien nunc, vel efficitur urna malesuada nec. Fusce vulputate ornare congue. Proin vulputate lacus lorem, vitae dignissim massa luctus eget. Nam ante libero, ornare eu enim eu, vulputate suscipit nulla. Donec consectetur, dui vel malesuada ullamcorper, metus sem dignissim nunc, et varius nisl est sit amet nisl. Quisque placerat feugiat sapien, id vulputate turpis dignissim id. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec mauris ante, viverra nec sem ac, interdum sollicitudin nisl.'),
            cls="container-section"
        ),
        footer(links={'Follow me on Twitter': 'https://x.com/dgwyer'}),
    )

### Login Routes ###

@rt("/login")
def get(sess):
    user_info, links = header_html(sess)

    frm = Form(
        Input(id='name', type="text", placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button(
            'Login',
            cls='btn'
        ),
        cls='mt-10 flex gap-x-2 items-center justify-center',
        action='/login',
        method='post'
    )

    return (
        header(links=links),
        Div(
            frm,
            cls="container-section"
        ),
        footer(links={'Follow me on Twitter': 'https://x.com/dgwyer'}),
    ),

@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    try: u = users[login.name]
    # If the primary key does not exist, the method raises a `NotFoundError`.
    # Here we use this to just generate a user -- in practice you'd probably to redirect to a signup page.
    except NotFoundError: u = users.insert(login)
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    # Because the session is signed, we can securely add information to it. It's stored in the browser cookies.
    # If you don't pass a secret signing key to `FastHTML`, it will auto-generate one and store it in a file `./sesskey`.
    sess['auth'] = u.name
    intended_url = sess.pop('intended_url', '/')
    
    return RedirectResponse(intended_url, status_code=303)

### Logout Routes ###

@rt("/logout")
def get(sess):
    del sess['auth']
    return home_redir

### Todo Routes ###

# By including the `auth` parameter, it gets passed the current username, for displaying in the title.
@rt("/todos")
def get(auth, sess):
    title = f"{auth}'s Todo list"
    top = Grid(H1(title), Div(A('logout', href='/logout'), style='text-align: right'))
    # We don't normally need separate "screens" for adding or editing data. Here for instance,
    # we're using an `hx-post` to add a new todo, which is added to the start of the list (using 'afterbegin').
    new_inp = Input(id="new-title", name="title", type="text", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add", cls='btn')),
               hx_post="/todos", target_id='todo-list', hx_swap="afterbegin", cls="mb-12")
    items = Tbody(*todos(order_by='priority'),
               id='todo-list', cls='sortable divide-y divide-gray-200')
    # We create an empty 'current-todo' Div at the bottom of our page, as a target for the details and editing views.
    card = Card(Ul(items), header=add, footer=Div(id='current-todo'))
    user_info, links = header_html(sess)

    return (
        header(links=links),
        Div(
            add,
            Table(
                Thead(
                    Tr(
                        Th('Title', scope='col', cls='min-w-[180px] pr-3 py-3.5 text-left text-sm font-semibold text-gray-900'),
                        Th('ToDo', scope='col', cls='min-w-[300px] max-w-[500px] pr-3 py-3.5 text-left text-sm font-semibold text-gray-900'),
                        Th('Done', scope='col', cls='min-w-[100px] pr-3 py-3.5 text-left text-sm font-semibold text-gray-900'),
                        Th(
                            Span('Edit', cls='sr-only'),
                            scope='col',
                            cls='relative py-3.5 pl-3 pr-4 sm:pr-0'
                        )
                    )
                ),
                items,
                cls='min-w-fit divide-y divide-gray-300'
            ),
            Div(id='current-todo'),
            cls="container-section"
        ),
        footer(links={'Follow me on Twitter': 'https://x.com/dgwyer'}),
    )

# This route handler uses a path parameter `{id}` which is automatically parsed and passed as an int.
@rt("/todos/{id}")
def delete(id:int):
    todos.delete(id)
    return clr_details()

@rt("/edit/{id}")
def get(id:int):
    res = Form(
        Group(Input(id="title", type="text"),
        Button("Save", cls='btn'),
        Button("Cancel", hx_get="/todos/cancel", hx_target="#edit", cls='btn')),
        Hidden(id="id"),
        CheckboxX(id="done", label='Done'),
        Textarea(id="details", name="details", rows=10),
        Button('Delete', hx_delete=f'/todos/{id}', hx_target=f'#todo-{id}', hx_swap="outerHTML", cls='btn'),
        hx_put="/todos", hx_swap="outerHTML", hx_target=f'#todo-{id}', id="edit")
    # `fill_form` populates the form with existing todo data, and returns the result.
    # Indexing into a table (`todos`) queries by primary key, which is `id` here. It also includes
    # `xtra`, so this will only return the id if it belongs to the current user.
    return fill_form(res, todos[id])

@app.get("/todos/cancel")
def cancel():
    return clr_details()

@rt("/todos")
def put(todo: Todo):
    if todo.title == '' or todo.title is None:
        return None

    # `update` is part of the MiniDataAPI spec.
    # Note that the updated todo is returned. By returning the updated todo, we can update the list directly.
    # Because we return a tuple with `clr_details()`, the details view is also cleared.
    return todos.update(todo), clr_details()

@rt("/todos")
def post(todo:Todo):
    if todo.title == '' or todo.title is None:
        return None

    # `hx_swap_oob='true'` tells HTMX to perform an out-of-band swap, updating this element wherever it appears.
    # This is used to clear the input field after adding the new todo.
    new_inp =  Input(id="new-title", name="title", type="text", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the start of the list, because we used
    # `hx_swap='afterbegin'` when creating the todo list form.
    return todos.insert(todo), new_inp

@rt("/todos/{id}")
def get(id:int):
    todo = todos[id]
    # `hx_swap` determines how the update should occur. We use "outerHTML" to replace the entire todo `Li` element.
    btn = Button('Delete', hx_delete=f'/todos/{todo.id}',
                 target_id=f'todo-{todo.id}', hx_swap="outerHTML", cls='btn')
    return Div(H2(todo.title), Div(todo.details, cls="p-2"), btn)

### Process Static Files ###

@rt("/{fname:path}.{ext:static}")
def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# Start the Python web server, SQLite editor, Jupyter Lab server, and Tailwind CSS compiler.
def serve_dev(db=False, jupyter=False, tw=False, db_path='data/main.db', sqlite_port=8035, jupyter_port=8036, tw_src='./src/app.css', tw_dist='./public/app.css'):
    print("Starting servers...")
    if db:
        print("Starting SQLite...")
        sqlite_process = subprocess.Popen(
            ['sqlite_web', db_path, '--port', str(sqlite_port), '--no-browser'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f'SQLite: http://localhost:{sqlite_port}')

    if jupyter:
        print("Starting Jupyter...")
        jupyter_process = subprocess.Popen(
            ['jupyter', 'lab', '--port', str(jupyter_port), '--no-browser', '--NotebookApp.token=', '--NotebookApp.password='],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
            text=True
        )

        # Extract and print the Jupyter Lab URL
        for line in jupyter_process.stderr:
            if 'http://' in line:
                match = re.search(r'(http://localhost:\d+/lab)', line)
                if match:
                    print(f'Jupyter Lab: {match.group(1)}')
                    break

    if tw:
        print("Starting Tailwind...")
        tailwind_process = subprocess.Popen(
            ['tailwindcss', '-i', tw_src, '-o', tw_dist, '--watch'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    try:
        print("Starting FastAPI...")
        serve(reload_includes=["*.css"])
    finally:
        if db:
            sqlite_process.terminate()
        if jupyter:
            jupyter_process.terminate()
        if tw:
            tailwind_process.terminate()

serve_dev(db=True, tw=True, jupyter=True)
#serve()
