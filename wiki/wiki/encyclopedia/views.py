from markdown2 import markdown
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

def index(request):
    if request.method == "POST":
        query = request.POST['q'].lower()
        entries_list = [entry.lower() for entry in util.list_entries()] # I don't like this :(
        
        if entries_list.count(query) == 0:
            return results_view(request, query)
        
        return entry_view(request, query)
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_view(request, entry_name):
    markdown_source = util.get_entry(entry_name)
    
    if markdown_source is not None:
        html = markdown(markdown_source)
        return render(request, "encyclopedia/entry_page.html", {
            "entry_name": entry_name,
            "html": html
        })
    return render(request, "encyclopedia/entry_page.html", {
        "error_message": "The requested entry does not exist."
    })

def results_view(request, query):
    search_results = [entry for entry in util.list_entries() if query in entry.lower()]
    return render(request, "encyclopedia/results.html", {
        "search_results": search_results,
    })

def create_view(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        
        if title in util.list_entries():
            return render(request, "encyclopedia/create.html", {
                "message": "The entered item already exists in the wiki. sadge"
            })
        
        html = "#" + title + "\n\n" + content
        file_directory = "../entries/" + title + ".md"

        with open(file_directory, "w") as new_page:
            new_page.write(html)

        return render(request, "encyclopedia/entry_page.html", {
            "entry_name": title,
            "html": html
        })
    return render(request, "encyclopedia/create.html")

def create_new_page(title, content):
    title_html = "<h1>" + title + "</h1>\n"
    return title_html + content