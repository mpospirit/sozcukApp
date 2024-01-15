from django.shortcuts import render, redirect
from .models import Competitors, Words, Visitors
from datetime import datetime, timedelta
import json
from . import slack

SLACK = slack.Slack()
TIMEZONE_DIFFERENCE = 3
BAD_WORDS = [
    "ambiti",
    "amcık",
    "amck",
    "amık",
    "amını",
    "amına",
    "amında",
    "amsalak",
    "anüs",
    "dalyarak",
    "daşak",
    "daşağı",
    "daşşak",
    "daşşağı",
    "domal",
    "fahişe",
    "folloş",
    "fuck",
    "gavat",
    "godoş",
    "göt",
    "hasiktir",
    "hassiktir",
    "ibne",
    "ipne",
    "kahpe",
    "kahbe",
    "kaltak",
    "kaltağ",
    "kancık",
    "kancığ",
    "kavat",
    "kerane",
    "kerhane",
    "kevaşe",
    "mastırbasyon",
    "masturbasyon",
    "mastürbasyon",
    "orosbu",
    "orospu",
    "orusbu",
    "oruspu",
    "orsp",
    "pezevenk",
    "pzvnk",
    "puşt",
    "qavat",
    "sakso",
    "sıçar",
    "sıçayım",
    "sıçmak",
    "sıçsın",
    "sikem",
    "siker",
    "sikeyim",
    "sikici",
    "sikik",
    "sikim",
    "sikiş",
    "sikle",
    "sikme",
    "siktir",
    "sktr",
    "siktiği",
    "sokarım",
    "sokayım",
    "sürtük",
    "sperm",
    "taşak",
    "taşağa",
    "taşağı",
    "taşşak",
    "taşşağa",
    "taşşağı",
    "vajina",
    "yalaka",
    "yarağ",
    "yarra",
    "yrrk",
    "am",
    "aq",
    "a.q",
    "a.q.",
    "amk",
    "çük",
    "döl",
    "meme",
    "oç",
    "o.ç",
    "o.ç.",
    "oral",
    "penis",
    "piç",
    "pipi",
    "sik",
    "yarak",
    "am",
    "amcığa",
    "amcığı",
    "amcığın",
    "amcık",
    "amcıklar",
    "amcıklara",
    "amcıklarda",
    "amcıklardan",
    "amcıkları",
    "amcıkların",
    "amcıkta",
    "amcıktan",
    "amı",
    "amlar",
    "göt",
    "göte",
    "götler",
    "götlerde",
    "götlerden",
    "götlere",
    "götleri",
    "götlerin",
    "götte",
    "götten",
    "götü",
    "götün",
    "götveren",
    "götverende",
    "götverenden",
    "götverene",
    "götvereni",
    "götverenin",
    "götverenler",
    "götverenlerde",
    "götverenlerden",
    "götverenlere",
    "götverenleri",
    "götverenlerin",
    "kaltağa",
    "kaltağı",
    "kaltağın",
    "kaltak",
    "kaltaklar",
    "kaltaklara",
    "kaltaklarda",
    "kaltaklardan",
    "kaltakları",
    "kaltakların",
    "kaltakta",
    "kaltaktan",
    "orospu",
    "orospuda",
    "orospudan",
    "orospular",
    "orospulara",
    "orospularda",
    "orospulardan",
    "orospuları",
    "orospuların",
    "orospunun",
    "orospuya",
    "orospuyu",
    "otuz birci",
    "otuz bircide",
    "otuz birciden",
    "otuz birciler",
    "otuz bircilerde",
    "otuz bircilerden",
    "otuz bircilere",
    "otuz bircileri",
    "otuz bircilerin",
    "otuz bircinin",
    "otuz birciye",
    "otuz birciyi",
    "otuzbirci",
    "otuzbircide",
    "otuzbirciden",
    "otuzbirciler",
    "otuzbircilerde",
    "otuzbircilerden",
    "otuzbircilere",
    "otuzbircileri",
    "otuzbircilerin",
    "otuzbircinin",
    "otuzbirciye",
    "otuzbirciyi",
    "saksocu",
    "saksocuda",
    "saksocudan",
    "saksocular",
    "saksoculara",
    "saksocularda",
    "saksoculardan",
    "saksocuları",
    "saksocuların",
    "saksocunun",
    "saksocuya",
    "saksocuyu",
    "sıçmak",
    "sik",
    "sike",
    "siker sikmez",
    "siki",
    "sikilir sikilmez",
    "sikin",
    "sikler",
    "siklerde",
    "siklerden",
    "siklere",
    "sikleri",
    "siklerin",
    "sikmek",
    "sikmemek",
    "sikte",
    "sikten",
    "siktir",
    "siktirir siktirmez",
    "taşağa",
    "taşağı",
    "taşağın",
    "taşak",
    "taşaklar",
    "taşaklara",
    "taşaklarda",
    "taşaklardan",
    "taşakları",
    "taşakların",
    "taşakta",
    "taşaktan",
    "yarağa",
    "yarağı",
    "yarağın",
    "yarak",
    "yaraklar",
    "yaraklara",
    "yaraklarda",
    "yaraklardan",
    "yarakları",
    "yarakların",
    "yarakta",
    "yaraktan",
    "2g1c",
    "2 girls 1 cup",
    "acrotomophilia",
    "alabama hot pocket",
    "alaskan pipeline",
    "anal",
    "anilingus",
    "anus",
    "apeshit",
    "arsehole",
    "ass",
    "asshole",
    "assmunch",
    "auto erotic",
    "autoerotic",
    "babeland",
    "baby batter",
    "baby juice",
    "ball gag",
    "ball gravy",
    "ball kicking",
    "ball licking",
    "ball sack",
    "ball sucking",
    "bangbros",
    "bangbus",
    "bareback",
    "barely legal",
    "barenaked",
    "bastard",
    "bastardo",
    "bastinado",
    "bbw",
    "bdsm",
    "beaner",
    "beaners",
    "beaver cleaver",
    "beaver lips",
    "beastiality",
    "bestiality",
    "big black",
    "big breasts",
    "big knockers",
    "big tits",
    "bimbos",
    "birdlock",
    "bitch",
    "bitches",
    "black cock",
    "blonde action",
    "blonde on blonde action",
    "blowjob",
    "blow job",
    "blow your load",
    "blue waffle",
    "blumpkin",
    "bollocks",
    "bondage",
    "boner",
    "boob",
    "boobs",
    "booty call",
    "brown showers",
    "brunette action",
    "bukkake",
    "bulldyke",
    "bullet vibe",
    "bullshit",
    "bung hole",
    "bunghole",
    "busty",
    "butt",
    "buttcheeks",
    "butthole",
    "camel toe",
    "camgirl",
    "camslut",
    "camwhore",
    "carpet muncher",
    "carpetmuncher",
    "chocolate rosebuds",
    "cialis",
    "circlejerk",
    "cleveland steamer",
    "clit",
    "clitoris",
    "clover clamps",
    "clusterfuck",
    "cock",
    "cocks",
    "coprolagnia",
    "coprophilia",
    "cornhole",
    "coon",
    "coons",
    "creampie",
    "cum",
    "cumming",
    "cumshot",
    "cumshots",
    "cunnilingus",
    "cunt",
    "darkie",
    "date rape",
    "daterape",
    "deep throat",
    "deepthroat",
    "dendrophilia",
    "dick",
    "dildo",
    "dingleberry",
    "dingleberries",
    "dirty pillows",
    "dirty sanchez",
    "doggie style",
    "doggiestyle",
    "doggy style",
    "doggystyle",
    "dog style",
    "dolcett",
    "domination",
    "dominatrix",
    "dommes",
    "donkey punch",
    "double dong",
    "double penetration",
    "dp action",
    "dry hump",
    "dvda",
    "eat my ass",
    "ecchi",
    "ejaculation",
    "erotic",
    "erotism",
    "escort",
    "eunuch",
    "fag",
    "faggot",
    "fecal",
    "felch",
    "fellatio",
    "feltch",
    "female squirting",
    "femdom",
    "figging",
    "fingerbang",
    "fingering",
    "fisting",
    "foot fetish",
    "footjob",
    "frotting",
    "fuck",
    "fuck buttons",
    "fuckin",
    "fucking",
    "fucktards",
    "fudge packer",
    "fudgepacker",
    "futanari",
    "gangbang",
    "gang bang",
    "gay sex",
    "genitals",
    "giant cock",
    "girl on",
    "girl on top",
    "girls gone wild",
    "goatcx",
    "goatse",
    "god damn",
    "gokkun",
    "golden shower",
    "goodpoop",
    "goo girl",
    "goregasm",
    "grope",
    "group sex",
    "g-spot",
    "guro",
    "hand job",
    "handjob",
    "hard core",
    "hardcore",
    "hentai",
    "homoerotic",
    "honkey",
    "hooker",
    "horny",
    "hot carl",
    "hot chick",
    "how to kill",
    "how to murder",
    "huge fat",
    "humping",
    "incest",
    "intercourse",
    "jack off",
    "jail bait",
    "jailbait",
    "jelly donut",
    "jerk off",
    "jigaboo",
    "jiggaboo",
    "jiggerboo",
    "jizz",
    "juggs",
    "kike",
    "kinbaku",
    "kinkster",
    "kinky",
    "knobbing",
    "leather restraint",
    "leather straight jacket",
    "lemon party",
    "livesex",
    "lolita",
    "lovemaking",
    "make me come",
    "male squirting",
    "masturbate",
    "masturbating",
    "masturbation",
    "menage a trois",
    "milf",
    "missionary position",
    "mong",
    "motherfucker",
    "mound of venus",
    "mr hands",
    "muff diver",
    "muffdiving",
    "nambla",
    "nawashi",
    "negro",
    "neonazi",
    "nigga",
    "nigger",
    "nig nog",
    "nimphomania",
    "nipple",
    "nipples",
    "nsfw",
    "nsfw images",
    "nude",
    "nudity",
    "nutten",
    "nympho",
    "nymphomania",
    "octopussy",
    "omorashi",
    "one cup two girls",
    "one guy one jar",
    "orgasm",
    "orgy",
    "paedophile",
    "paki",
    "panties",
    "panty",
    "pedobear",
    "pedophile",
    "pegging",
    "penis",
    "phone sex",
    "piece of shit",
    "pikey",
    "pissing",
    "piss pig",
    "pisspig",
    "playboy",
    "pleasure chest",
    "pole smoker",
    "ponyplay",
    "poof",
    "poon",
    "poontang",
    "punany",
    "poop chute",
    "poopchute",
    "porn",
    "porno",
    "pornography",
    "prince albert piercing",
    "pthc",
    "pubes",
    "pussy",
    "queaf",
    "queef",
    "quim",
    "raghead",
    "raging boner",
    "rape",
    "raping",
    "rapist",
    "rectum",
    "reverse cowgirl",
    "rimjob",
    "rimming",
    "rosy palm",
    "rosy palm and her 5 sisters",
    "rusty trombone",
    "sadism",
    "santorum",
    "scat",
    "schlong",
    "scissoring",
    "semen",
    "sex",
    "sexcam",
    "sexo",
    "sexy",
    "sexual",
    "sexually",
    "sexuality",
    "shaved beaver",
    "shaved pussy",
    "shemale",
    "shibari",
    "shit",
    "shitblimp",
    "shitty",
    "shota",
    "shrimping",
    "skeet",
    "slanteye",
    "slut",
    "s&m",
    "smut",
    "snatch",
    "snowballing",
    "sodomize",
    "sodomy",
    "spastic",
    "spic",
    "splooge",
    "splooge moose",
    "spooge",
    "spread legs",
    "spunk",
    "strap on",
    "strapon",
    "strappado",
    "strip club",
    "style doggy",
    "suck",
    "sucks",
    "suicide girls",
    "sultry women",
    "swastika",
    "swinger",
    "tainted love",
    "taste my",
    "tea bagging",
    "threesome",
    "throating",
    "thumbzilla",
    "tied up",
    "tight white",
    "tit",
    "tits",
    "titties",
    "titty",
    "tongue in a",
    "topless",
    "tosser",
    "towelhead",
    "tranny",
    "tribadism",
    "tub girl",
    "tubgirl",
    "tushy",
    "twat",
    "twink",
    "twinkie",
    "two girls one cup",
    "undressing",
    "upskirt",
    "urethra play",
    "urophilia",
    "vagina",
    "venus mound",
    "viagra",
    "vibrator",
    "violet wand",
    "vorarephilia",
    "voyeur",
    "voyeurweb",
    "voyuer",
    "vulva",
    "wank",
    "wetback",
    "wet dream",
    "white power",
    "whore",
    "worldsex",
    "wrapping men",
    "wrinkled starfish",
    "xx",
    "xxx",
    "yaoi",
    "yellow showers",
    "yiffy",
    "zoophilia",
    "🖕",
]

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
