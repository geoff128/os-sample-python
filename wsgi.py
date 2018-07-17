from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello():
    return "[11:25 15.07.2018] Działa"

if __name__ == "__main__":
    application.run()
'''
TOKEN = 'NDU5OTc1NDE2NTE0MzQ3MDA4.Dg-BFw.s7130edXTLByJAAyMdVmlIS5JI8'
ID = '459975416514347008'
CLEAR_IDs = ['393837938372378629', '267343850433937408']

PREFIX = '/'

client = Bot(PREFIX)

commands = [['pomoc', 'wyświetla tę wiadomość'], ['rng', 'losuje liczbę z zakresu {0, 2\'147\'483\'647}'], ['rng [zakres_do]', 'losuje liczbę z zakresu {0, *zakres_do*}'], ['rng [zakres_od] [zakres_do]', 'losuje liczbę z zakresu {*zakres_od*, *zakres_do*}'], ['pogoda', 'wyświetla pogodę dla Warszawy'], ['pogoda [miasto]', 'wyświetla pogodę dla danego miasta'], ['clear, cs [n=1]', 'usuwa *n* wiadomości [1 ≥ n ≥ 100]'], ['userinfo, uinfo, ui [ID=@me]', 'wyświetla info o użytkowniku z podanym ID, domyślnie - autora wiadomości'], ['botinfo, bifno', 'wyświetla informacje o tym bocie']]


weather = Weather(unit=Unit.CELSIUS)

conditions_EN_PL = {'tornado': 'tornado',
                   'tropical storm': 'deszcz tropikalny',
                   'hurricane': 'huragan',
                   'severe thunderstorms': 'silne burze',
                   'thunderstorms': 'burze z piorunami',
                   'mixed rain and snow': 'deszcz ze śniegiem',
                   'mixed rain and sleet': 'deszcz ze śniegiem',
                   'mixed snow and sleet': 'deszcz ze śniegiem',
                   'freezing drizzle': 'marznąca mżawka',
                   'drizzle': 'mżawka',
                   'freezing rain': 'marznący deszcz',
                   'showers': 'przelotne deszcze',
                   'snow flurries': 'podmuchy śniegu',
                   'light snow showers': 'przelotne opady śniegu',
                   'blowing snow': 'zamieć śnieżna',
                   'rain': 'deszczowo',
                   'snow': 'opady śniegu',
                   'hail': 'grad',
                   'sleet': 'deszcz ze śniegiem',
                   'dust': 'burza piaskowa',
                   'foggy': 'mgliście',
                   'haze': 'mgła',
                   'smoky': 'smog',
                   'blustery': 'porywisty wiatr',
                   'windy': 'wietrznie',
                   'cold': 'zimno',
                   'cloudy': 'pochmurnie',
                   'mostly sunny': 'bezchmurnie',
                   'partly sunny': 'przejaśnienia',
                   'mostly cloudy': 'całkowite zachmurzenie',
                   'partly cloudy': 'częściowe zachmurzenie',
                   'clear': 'przejrzyście',
                   'sunny': 'słonecznie',
                   'fair': '',
                   'mixed rain and hail': 'deszcz z gradem',
                   'hot': 'upał',
                   'isolated thunderstorms': 'pojedyncze burze',
                   'scattered thunderstorms': 'przelotne burze',
                   'scattered showers': 'przelotne deszcze',
                   'scattered snow showers': 'przelotne opady śniegu',
                   'heavy snow': 'śnieżyca',
                   'thundershowers': 'burza z piorunami',
                   'snow showers': 'przelotne opady śniegu',
                   'not available': 'niedostępne'}

mies_EN_PL = {'Jan': 'Stycznia',
              'Feb': 'Lutego',
              'Mar': 'Marca',
              'Apr': 'Kwietnia',
              'May': 'Maja',
              'Jun': 'Czerwca',
              'Jul': 'Lipca',
              'Aug': 'Sierpnia',
              'Sep': 'Września',
              'Oct': 'Października',
              'Nov': 'Listopada',
              'Dec': 'Grudnia'}

def error(text=discord.Embed.Empty, ft=discord.Embed.Empty):
    embed = discord.Embed(title="ERROR", description=text, colour=0xcc0000)
    embed.set_footer(text=ft)
    return embed

def info(text=discord.Embed.Empty, ft=discord.Embed.Empty):
    embed = discord.Embed(title="INFO", description=text, colour=0x4285f4)
    embed.set_footer(text=ft)
    return embed

### KOMENDY ###

@client.command(pass_context=True)
async def pomoc(ctx):
    msg = ''
    for c in commands:
        msg += '' + PREFIX + c[0] + '    (' + c[1] + ')\n'
    await client.send_message(ctx.message.channel, embed=info(msg))

@client.command(pass_context=True)
async def rng(ctx, arg1='', arg2=''):
    start = 0; stop = 2147483647
    if arg1!='' and arg2=='':
        stop = int(arg1)
    if arg1!='' and arg2!='':
        start = int(arg1)
        stop = int(arg2)
    num = random.randint(start, stop)
    msg = 'Wylosowana liczba to {}'.format(str(num))
    await client.send_message(ctx.message.channel, msg)

@client.command(pass_context=True)
async def pogoda(ctx, city='Warszawa'):
    location = weather.lookup_by_location(city)
    if location is not None:
        forecasts = location.forecast
        forecast = forecasts[0]
        print( forecast )
        date = forecast.date.split(' ')
        msg = city.capitalize() + ', ' + date[0] + ' ' + mies_EN_PL[date[1]] + ' ' + date[2] + ':\n'
        msg +=  'od: ' + forecast.low + '°C, do ' + forecast.high + '°C\n'
        msg += conditions_EN_PL[forecast.text.lower()].capitalize()
        await client.send_message(ctx.message.channel, msg)
    else:
        msg = 'Nie znaleziono miasta {}'.format(city)
        await client.send_message(ctx.message.channel, msg)

@client.command(pass_context = True, aliases=['cs'])
async def clear(ctx, number='1'):
    try:
        number = int(number)
    except ValueError:
        await client.send_message(ctx.message.channel, embed=error('Nie możesz tego zrobić', 'Szaleńcze...'))
        
    if ctx.message.author.id not in CLEAR_IDs and ctx.message.channel.id != '464120639649742858':
        await client.send_typing(ctx.message.channel)
        await client.send_message(ctx.message.channel, embed=error('Nie możesz tego zrobić', 'Komenda dostępna wyłącznie dla For The Horde#3893 oraz Tomasz#3539'))
        return
    msgs = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit=number):
        msgs.append(x)
    if number == 1:
        await client.delete_message(msgs[0])
    else:   
        await client.delete_messages(msgs)


@client.command(pass_context = True,  aliases=['ui', 'uinfo'])
async def userinfo(ctx, uid='@me'):
    if uid == '@me':
        user = discord.Server.get_member(ctx.message.server, user_id=ctx.message.author.id)
    else:
        user = discord.Server.get_member(ctx.message.server, user_id=uid)
    if user is None:
        await client.send_message(ctx.message.channel, embed=error('Nie ma takiego użytkownika'))

    
    embed = discord.Embed(title=user.name, description='Informacje o użytkowniku:', colour=0x00cc00)
    embed.add_field(name='Konto utworzone', value=user.created_at, inline=False)
    embed.add_field(name='Nick na serwerze', value=user.display_name, inline=False)
    embed.add_field(name='Do serwera dołączył', value=user.joined_at, inline=False)
    if user.game is not None:
        embed.add_field(name='W grze', value=user.game, inline=False)

    embed.set_image(url=user.avatar_url)
    await client.send_message(ctx.message.channel, embed=embed)

@client.command(pass_context = True,  aliases=['binfo'])
async def botinfo(ctx):
    user = discord.Server.get_member(ctx.message.server, user_id=ID)
    if user is None:
        await client.send_message(ctx.message.channel, embed=error('Wystąpił błąd'))

    
    embed = discord.Embed(title=user.name, description='Informacje o bocie:', colour=0x00aa00)
    embed.add_field(name='Twórca', value='Tomasz#3539', inline=False)
    embed.add_field(name='Konto utworzone', value=user.created_at, inline=False)
    embed.add_field(name='Nick na serwerze', value=user.display_name, inline=False)
    embed.add_field(name='Do serwera dołączył', value=user.joined_at, inline=False)
    embed.add_field(name='Prefix', value=PREFIX, inline=False)
    embed.add_field(name='Dostępne komendy', value=len(commands), inline=False)
    await client.send_message(ctx.message.channel, embed=embed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

    print(message.channel)

    uMsg = message.content    

    if uMsg.lower().replace('z', 'ż').startswith('boże'):
        msg = 'Tak?'
        await client.send_message(message.channel, msg)

    if uMsg.lower().startswith('co'):
        msg = 'Pszenżyto'
        await client.send_message(message.channel, msg)

    if uMsg.startswith('<@' + ID + '>'):
        msg = 'Do usług'
        await client.send_message(message.channel, msg)

    if uMsg.lower().find('muw') != -1:
        splMsg = uMsg.split(' ')
        popr = ''
        for slowo in splMsg:
            if slowo.lower().find('muw') != -1:
                popr += '\*' + slowo.lower().replace('u', 'ó') + ', '
        msg = popr[:-2]
        await client.send_message(message.channel, msg)

    if uMsg.lower().find('nbpjc') != -1:
        msg = 'NWWA'
        await client.send_message(message.channel, msg)

    if 'd' in uMsg:
        splMsg = uMsg.split('d')
        if int(splMsg[0]) < 0:
            await client.send_message(ctx.message.channel, embed=error('Nie możesz tego zrobić', 'Szaleńcze...'))
            return
        if int(splMsg[0]) == 0:
            msg = 'OK, nic nie losuję...'
            await client.send_message(message.channel, msg)
            return 
        if(len(splMsg) == 2):
            nums = []
            for i in range( int(splMsg[0]) ):
                num = random.randrange(1, (int(splMsg[1])+1))
                nums.append( str(num) )
            msg = 'Wylosowane liczby to {}'.format( ', '.join(nums) )
            await client.send_message(message.channel, msg)
            

### INI ###

@client.event
async def on_ready():
    print('Zalogowany jako: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('------')

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Serwery:")
        for server in client.servers:
            print(server.name)
        print('------')
        await asyncio.sleep(600)

client.loop.create_task(list_servers())


async def background_loop():
    await client.wait_until_ready()
    while not client.is_closed:
        gameName = "not a bot"
        gameName = "".join( random.choice([k.upper(), k ]) for k in gameName )
        await client.change_presence(game = Game(name = gameName))
        await asyncio.sleep(0.7)

client.loop.create_task(background_loop())


client.run(TOKEN)'''
