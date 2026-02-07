[...]
@app.route('/admin/flag')
def admin_flag():
    x_fetcher = request.headers.get('X-Fetcher', '').lower()
    if x_fetcher == 'internal':
        return f"""<html><h1>NOT OK</h1></html>""", 403
    if not is_localhost(request.remote_addr):
        return f"""<html><h1>NOT OK</h1></html>""", 403
    index = request.args.get('i',0, type=int)
    char = request.args.get('c','', type=str)
    if index < 0 or index >= len(FLAG):
        return f"""<html><h1>NOT OK</h1></html>""", 404
    if len(char) != 1:
        return f"""<html><h1>NOT OK</h1></html>""", 404
    if FLAG[index] != char:
        return f"""<html><h1>NOT OK</h1></html>""", 404
    return f"""<html><h1>OK</h1></html>"""
[...]