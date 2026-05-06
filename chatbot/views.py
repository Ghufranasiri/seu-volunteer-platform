from django.shortcuts import render


def chat_view(request):
    return render(request, "chatbot/chat.html")


def chatbot_page(request):
    return render(request, "chatbot/chat.html")