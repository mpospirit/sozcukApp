from django.shortcuts import render, redirect
from .models import Competitors, Words, Visitors
from datetime import datetime, timedelta
import json
from . import slack
import pandas as pd

SLACK = slack.Slack()
TIMEZONE_DIFFERENCE = 3
BAD_WORDS = pd.read_csv("bad_words.csv")["words"].tolist()

# Create your views here.
def index(request):
    timezone_difference_today = (
        datetime.now() + timedelta(hours=TIMEZONE_DIFFERENCE)
    ).date()
    timezone_difference_yesterday = (
        datetime.now() + timedelta(hours=TIMEZONE_DIFFERENCE) - timedelta(days=1)
    ).date()

    competitors = Competitors.objects.filter(
        dateCreated__date=timezone_difference_today
    ).order_by("-score")[:10]
    competitor_count = Competitors.objects.filter(
        dateCreated__date=timezone_difference_today
    ).count()

    words_yesterday = Words.objects.filter(
        releaseDate__date=timezone_difference_yesterday
    ).order_by("length")

    meta = request.META

    if "HTTP_CF_CONNECTING_IP" in meta:
        meta_ip = meta["HTTP_CF_CONNECTING_IP"]
    else:
        meta_ip = "localhost"
    
    if 'HTTP_USER_AGENT' in meta:
        meta_agent = meta['HTTP_USER_AGENT']
    else:
        meta_agent = None

    Visitors.objects.create(
        ip=meta_ip,
        agent=meta_agent,
        dateCreated=datetime.now() + timedelta(hours=TIMEZONE_DIFFERENCE),
    )


    context = {
        "competitors": competitors,
        "competitor_count": competitor_count,
        "words_yesterday": words_yesterday,
        "now": datetime.now() + timedelta(hours=TIMEZONE_DIFFERENCE),
        "yesterday": datetime.now()
        + timedelta(hours=TIMEZONE_DIFFERENCE)
        - timedelta(days=1),
    }

    return render(request, "core/index.html", context)


def about(request):
    return render(request, "core/about.html")


def help(request):
    return render(request, "core/help.html")


def competitors(request):
    timezone_difference_today = (
        datetime.now() + timedelta(hours=TIMEZONE_DIFFERENCE)
    ).date()

    competitors = Competitors.objects.filter(
        dateCreated__date=timezone_difference_today
    ).order_by("-score")

    context = {
        "competitors": competitors,
    }

    return render(request, "core/competitors.html", context)


def game(request):
    timezone_difference_today = (
        datetime.now() + timedelta(hours=TIMEZONE_DIFFERENCE)
    ).date()

    words = Words.objects.filter(releaseDate__date=timezone_difference_today).order_by(
        "length"
    )

    word_list = list(words.values())

    context = {
        "words": json.dumps(word_list, default=str),
    }

    name = request.POST.get("name")
    score = request.POST.get("score")
    
    dateCreated = datetime.now() + timedelta(hours=3)

    if name and score:
        if name in BAD_WORDS:
            competitor = Competitors(name="!#@$%", score=score, dateCreated=dateCreated)
            competitor.save()

            message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{name}* isimli kullanıcı, *{score}* puan ile oyunu tamamladı. Kullanıcı adı, uygunsuz içerik içerdiği için sisteme sansürlenerek kaydedildi.",
                    },
                }
            ]

            SLACK.send_message("#competitors", message)

            return redirect("core:index")

        else:
            competitor = Competitors(name=name, score=score, dateCreated=dateCreated)
            competitor.save()

            message = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{name}* isimli kullanıcı, *{score}* puan ile oyunu tamamladı.",
                    },
                }
            ]

            SLACK.send_message("#competitors", message)

            return redirect("core:index")

    return render(request, "core/game.html", context)

def custom_404(request, exception):
    return render(request, "core/404.html", status=404)
