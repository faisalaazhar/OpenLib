from django.shortcuts import render, redirect
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from django.core.files.storage import FileSystemStorage


# MongoDB Connect
db_client = pymongo.MongoClient("mongodb://localhost:27017")
db = db_client["django-library"]
blog_table = db["blog-post"]


# Create your views here.


def blogs(request):
    blog = []
    for data in blog_table.find():
        blog.append(data)
    return render(request, "blog/blog.html", {'blog': blog})


def addBlog(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST" and request.FILES['photo']:
            publishedAt = datetime.now()
            title = request.POST["title"]
            photo = request.FILES['photo']
            fss = FileSystemStorage()
            file = fss.save(photo.name, photo)
            file_url = fss.url(file)
            content = request.POST["content"]
            newBlog = {"title": title, "photo": file_url, "user": current_user.username,
                       "publishedAt": publishedAt, "updatedAt": publishedAt, "content": content}
            blog_table.insert_one(newBlog)
            return redirect('/blog')
        return render(request, "blog/addBlog.html")
    else:
        return redirect('/login')


def updateBlog(request, id):
    single_blog = blog_table.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        updatedAt = datetime.now()
        title = request.POST["title"]
        blog = request.POST["content"]
        updatedBlog = {'title': title, 'content': blog, 'updatedAt': updatedAt}
        filter = {'_id': ObjectId(id)}
        newvalues = {"$set": updatedBlog}
        blog_table.update_one(filter, newvalues, upsert=False)
        return redirect("/blog")
    return render(request, "blog/updateBlog.html", {'single_blog': single_blog})


def deleteBlog(request, id):
    if (blog_table.delete_one({"_id": ObjectId(id)})):
        return redirect("/blog")
    return redirect("/blog")


def blogSearch(request):
    blog = []
    if request.method == 'POST':
        word = request.POST["word"]
        blog_table.create_index([("title", "text"), ("content", "text")])
        for i in blog_table.find({"$text": {"$search": word}}):
            blog.append(i)
        return render(request, "blog/searchBlog.html", {'blog': blog, 'word': word})
    return redirect('/blog')
