from django.shortcuts import render

def chatbot_page(request):
    return render(request, "chatbot/chat.html")