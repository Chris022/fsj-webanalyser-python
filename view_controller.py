def view_main():
    f = open("html/main.py.html", "r")

    return f.read()

def view_results(url):
    f = open("html/results.py.html", "r")
    html = f.read()

    #replace vars
    html = html.replace("{$url}",str(url))

    return html
