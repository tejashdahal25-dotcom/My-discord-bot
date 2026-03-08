import discord
from keep_alive import keep_alive
keep_alive()
from discord.ext import commands
import random
import json
import time

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

users = {}
dark_mode = False
last_work = {}

# ===== JOBS (renamed to JOBS_DATA to avoid conflict) =====
JOBS_DATA = {
    "youtuber": (100, 300),
    "developer": (200, 500),
    "cashier": (50, 150),
    "gamer": (150, 400),
    "meme_lord": (250, 600),
    "night_shift_worker": (300, 700)
}

work_cooldown = 30

# ===== SAVE / LOAD =====
def save():
    with open("data.json", "w") as f:
        json.dump(users, f)

def load():
    global users
    try:
        with open("data.json", "r") as f:
            users = json.load(f)
    except:
        users = {}

load()

def create_user(uid):
    if uid not in users:
        users[uid] = {
            "coins": 100,  # Starting bonus
            "xp": 0,
            "job": None
        }

# ===== ROASTS =====
roasts = [
    "You don't need GPS. You're already lost in life.",
    "You don't have dumb ideas. Just long streaks of bad thinking.",
    "I'd say you're 'extra' but even DLC has value.",
    "You don't lose arguments. You just restart them badly.",
    "You don't need enemies. Your decisions handle that.",
    "You type like autocorrect gave up.",
    "Your brain runs on trial version.",
    "You radiate 'main character in a side quest' energy."
]

# ===== NORMAL JOKES =====
jokes = [
    "Why don't programmers like nature? Too many bugs.",
    "Why did the gamer bring a ladder? To reach the next level.",
    "Why did the WiFi break up? No connection.",
    "Why don't skeletons fight? They don't have the guts.",
    "I told my computer I needed a break… it froze.",
    "Why did the student eat homework? Teacher said it was a piece of cake.",
    "Parallel lines have so much in common… it's a shame they'll never meet.",
    "Why was the math book sad? Too many problems."
]

# ===== DARK JOKES =====
dark_jokes = [
    "My phone battery lasts longer than my motivation.",
    "I started a procrastinators club… we'll start tomorrow.",
    "My life didn't give lemons. It gave buffering.",
    "I tried being normal once. Worst decision ever.",
    "Brain at 3AM: Remember that cringe moment?",
    "If laziness were a job, I'd still be underqualified.",
    "My confidence left the chat years ago.",
    "Life tutorial skipped. Now playing on hard mode.",
    "I don't trip over my past. I replay it nightly.",
    "I don't rise and shine. I caffeinate and hope.",
    "My hobbies include overthinking and avoiding responsibilities.",
    "I whisper 'it is what it is' 40 times a day.",
    "I set 5 alarms just to ignore all of them.",
    "If overthinking burned calories I'd be shredded.",
    "My brain has 200 tabs open and none responding.",
    "I don't need a villain arc. I need sleep.",
    "My wallet and I are in a toxic relationship.",
    "I don't chase dreams. I watch them from bed.",
    "Adulthood is just side quests with bills.",
    "I thought I hit rock bottom. It had a basement."
]

# ===== NORMAL MEMES =====
memes = [
    "When teacher says 'any doubts?' and class becomes statue 🗿",
    "Me studying 5 minutes before exam like Olympic training.",
    "Opening fridge 10 times hoping new food spawns.",
    "Group project but it's solo mission.",
    "When WiFi disconnects during ranked 💀",
    "That one friend who says 'easy paper' and gets 32%.",
    "Me: I'll sleep early. Also me at 2AM:",
    "When exam question says 'easy' but it's in Greek."
]

# ===== DARK MEMES =====
dark_memes = [
    "POV: You check bank account for character development.",
    "Me pretending I understand life's plot.",
    "Trying to fix sleep schedule since 2017.",
    "When motivation loads slower than old WiFi.",
    "Brain at 3AM starting director's cut of regrets.",
    "When you say 'it's fine' but it's not.",
    "Me refreshing nothing hoping life updates.",
    "Adulthood is unpaid DLC.",
    "When you realize NPCs have better routines.",
    "Me speedrunning responsibilities (fail attempt).",
    "That moment you realize you are the side character.",
    "POV: You open fridge and it opens your sadness.",
    "Me checking notifications like maybe someone cares.",
    "Life said tutorial skipped.",
    "When your plans ghost you.",
    "Me looking for motivation like lost WiFi signal.",
    "Confidence.exe has stopped working.",
    "POV: It's Sunday night and reality loads.",
    "Me realizing sleep schedule is myth.",
    "Trying to upgrade life but no coins."
]

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Serving {len(bot.guilds)} servers')
    print('Bot is ready to use!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    uid = str(message.author.id)
    create_user(uid)
    users[uid]["xp"] += 5
    save()

    await bot.process_commands(message)

# ===== BASIC COMMANDS =====
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Bot is working!")

@bot.command()
async def roast(ctx):
    await ctx.send(random.choice(roasts))

@bot.command()
async def joke(ctx):
    if dark_mode:
        await ctx.send(random.choice(dark_jokes))
    else:
        await ctx.send(random.choice(jokes))

@bot.command()
async def meme(ctx):
    if dark_mode:
        await ctx.send(random.choice(dark_memes))
    else:
        await ctx.send(random.choice(memes))

@bot.command()
async def dark(ctx, mode=None):
    global dark_mode
    if mode is None:
        await ctx.send(f"Dark mode is currently {'ON' if dark_mode else 'OFF'}")
    elif mode.lower() == "on":
        dark_mode = True
        await ctx.send("🖤 Dark mode activated.")
    elif mode.lower() == "off":
        dark_mode = False
        await ctx.send("💡 Dark mode disabled.")
    else:
        await ctx.send("Use `!dark on` or `!dark off`")

@bot.command()
async def level(ctx):
    uid = str(ctx.author.id)
    create_user(uid)
    await ctx.send(f"📊 XP: {users[uid]['xp']}")

@bot.command()
async def balance(ctx):
    uid = str(ctx.author.id)
    create_user(uid)
    await ctx.send(f"💰 Coins: {users[uid]['coins']}")

# ===== FIXED ECONOMY COMMANDS =====
@bot.command()
async def jobs(ctx):
    job_list = "**💼 Available Jobs:**\n"
    for job in JOBS_DATA:  # Fixed: using JOBS_DATA instead of jobs
        min_pay, max_pay = JOBS_DATA[job]
        job_list += f"• **{job}** - {min_pay}-{max_pay} coins\n"
    await ctx.send(job_list)

@bot.command()
async def apply(ctx, *, job_name=None):
    if job_name is None:
        await ctx.send("❌ Please specify a job! Example: `!apply youtuber`")
        return
        
    uid = str(ctx.author.id)
    create_user(uid)
    
    job_name = job_name.lower().strip()
    
    if job_name not in JOBS_DATA:  # Fixed
        await ctx.send(f"❌ Job '{job_name}' doesn't exist. Use `!jobs` to see available jobs.")
        return
    
    users[uid]["job"] = job_name
    save()
    await ctx.send(f"✅ You are now a **{job_name}**!")

@bot.command()
async def work(ctx):
    uid = str(ctx.author.id)
    create_user(uid)
    
    if users[uid]["job"] is None:
        await ctx.send("❌ You don't have a job! Use `!jobs` and `!apply [job]` first.")
        return
    
    now = time.time()
    if uid in last_work and now - last_work[uid] < work_cooldown:
        remaining = int(work_cooldown - (now - last_work[uid]))
        minutes = remaining // 60
        seconds = remaining % 60
        await ctx.send(f"⏳ Wait {minutes}m {seconds}s before working again.")
        return
    
    min_pay, max_pay = JOBS_DATA[users[uid]["job"]]  # Fixed
    pay = random.randint(min_pay, max_pay)
    
    users[uid]["coins"] += pay
    last_work[uid] = now
    save()
    
    await ctx.send(f"💼 You worked as **{users[uid]['job']}** and earned **{pay} coins**! Total: {users[uid]['coins']}")

# ===== TEST COMMAND =====
@bot.command()
async def testdata(ctx):
    uid = str(ctx.author.id)
    create_user(uid)
    await ctx.send(f"📁 Your data: {users[uid]}")
# ===== GAMBLING COMMANDS =====
@bot.command()
async def coinflip(ctx, bet: int = None, choice: str = None):
    """Flip a coin - choose heads or tails"""
    uid = str(ctx.author.id)
    create_user(uid)
    
    if bet is None or choice is None:
        await ctx.send("❌ Example: `!coinflip 50 heads` or `!coinflip 50 tails`")
        return
    
    if bet < 10:
        await ctx.send("❌ Minimum bet is 10 coins!")
        return
    
    if users[uid]["coins"] < bet:
        await ctx.send(f"❌ You don't have enough coins! You have {users[uid]['coins']} coins.")
        return
    
    choice = choice.lower().strip()
    if choice not in ["heads", "tails", "h", "t"]:
        await ctx.send("❌ Choose `heads` or `tails`")
        return
    
    # Normalize choice
    if choice in ["h", "heads"]:
        choice = "heads"
    else:
        choice = "tails"
    
    # Flip coin
    flip = random.choice(["heads", "tails"])
    
    # Check win
    if flip == choice:
        users[uid]["coins"] += bet
        save()
        await ctx.send(f"🪙 Coin landed on **{flip}**! You won **{bet}** coins! New balance: {users[uid]['coins']}")
    else:
        users[uid]["coins"] -= bet
        save()
        await ctx.send(f"🪙 Coin landed on **{flip}**! You lost **{bet}** coins! New balance: {users[uid]['coins']}")

@bot.command()
async def roulette(ctx, bet: int = None, choice: str = None):
    """Play roulette - choose red, black, green, or a number (0-36)"""
    uid = str(ctx.author.id)
    create_user(uid)
    
    if bet is None or choice is None:
        await ctx.send("❌ Example: `!roulette 50 red` or `!roulette 100 7`")
        return
    
    if bet < 10:
        await ctx.send("❌ Minimum bet is 10 coins!")
        return
    
    if users[uid]["coins"] < bet:
        await ctx.send(f"❌ You don't have enough coins! You have {users[uid]['coins']} coins.")
        return
    
    choice = choice.lower().strip()
    
    # Roulette wheel numbers with colors
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    green_numbers = [0]
    
    # Spin the wheel
    spin = random.randint(0, 36)
    
    # Determine spin color
    if spin == 0:
        spin_color = "green"
    elif spin in red_numbers:
        spin_color = "red"
    else:
        spin_color = "black"
    
    # Check if choice is a number
    if choice.isdigit():
        number_choice = int(choice)
        if number_choice < 0 or number_choice > 36:
            await ctx.send("❌ Choose a number between 0 and 36")
            return
        
        if spin == number_choice:
            # Win big for exact number
            win_amount = bet * 35
            users[uid]["coins"] += win_amount
            save()
            await ctx.send(f"🎰 Roulette landed on **{spin} {spin_color}**! JACKPOT! You won **{win_amount}** coins! New balance: {users[uid]['coins']}")
        else:
            users[uid]["coins"] -= bet
            save()
            await ctx.send(f"🎰 Roulette landed on **{spin} {spin_color}**! You lost **{bet}** coins. New balance: {users[uid]['coins']}")
    
    # Check if choice is color
    elif choice in ["red", "black", "green"]:
        if spin_color == choice:
            if choice == "green":
                win_amount = bet * 35  # Green pays 35:1
            else:
                win_amount = bet  # Red/black pay 1:1
            
            users[uid]["coins"] += win_amount
            save()
            await ctx.send(f"🎰 Roulette landed on **{spin} {spin_color}**! You won **{win_amount}** coins! New balance: {users[uid]['coins']}")
        else:
            users[uid]["coins"] -= bet
            save()
            await ctx.send(f"🎰 Roulette landed on **{spin} {spin_color}**! You lost **{bet}** coins. New balance: {users[uid]['coins']}")
    
    else:
        await ctx.send("❌ Choose: `red`, `black`, `green`, or a number (0-36)")

@bot.command()
async def dice(ctx, bet: int = None):
    """Roll dice (1-100) - win if over 50"""
    uid = str(ctx.author.id)
    create_user(uid)
    
    if bet is None:
        await ctx.send("❌ Example: `!dice 50`")
        return
    
    if bet < 10:
        await ctx.send("❌ Minimum bet is 10 coins!")
        return
    
    if users[uid]["coins"] < bet:
        await ctx.send(f"❌ You don't have enough coins! You have {users[uid]['coins']} coins.")
        return
    
    roll = random.randint(1, 100)
    
    if roll > 50:
        users[uid]["coins"] += bet
        save()
        await ctx.send(f"🎲 You rolled **{roll}**! You won **{bet}** coins! New balance: {users[uid]['coins']}")
    else:
        users[uid]["coins"] -= bet
        save()
        await ctx.send(f"🎲 You rolled **{roll}**! You lost **{bet}** coins. New balance: {users[uid]['coins']}")
# ===== RUN BOT =====

import os
bot.run(os.environ['MTQ3NTQ2ODc1OTE1MzI1MDM2NA.GnXg6_.n_z8Oa6zw7qYgmv5vlxjzruKyRT3Xi6RvxkQTc'])
