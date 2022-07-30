# bot.py
import os
import random
import threading
import time
from dotenv import load_dotenv
from reminders import Reminders
from datetime import datetime, timedelta

# from crontabs import Cron, Tab

# 1
from discord.ext import commands, tasks
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')
rem=Reminders()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    reminder_task.start() # important to start the loop

@bot.command(name='rem-help', help='prints help information')
async def rem_help(ctx):
    response = rem.help()
    await ctx.send(response)

@bot.command(name='rem-create', help='create a new reminder')
async def create_reminder(ctx, user, interval, message):
    response = rem.create_reminder(user, interval, message, ctx.channel.id)
    await ctx.send(response)

@bot.command(name='rem-list', help='List all reminders and their IDs')
async def list_reminders(ctx):
    response = rem.list_reminders()
    await ctx.send(response)

@bot.command(name='rem-show-active', help='List all reminders and their IDs')
async def list_reminders(ctx):
    response = rem.get_active_reminders()
    await ctx.send(response)
    

@bot.command(name='rem-pause', help='Pause a reminder')
async def pause_reminder(ctx, reminder_id):
    response = rem.pause_reminder(reminder_id)
    await ctx.send(response)

@bot.command(name='rem-unpause', help='Unpause a reminder')
async def unpause_reminder(ctx, reminder_id):
    response = rem.unpause_reminder(reminder_id)
    await ctx.send(response)

@bot.command(name='rem-stop', help='Stop and delete a reminder')
async def delete_reminder(ctx, reminder_id):
    response = rem.delete_reminder(reminder_id)
    await ctx.send(response)

@bot.event
async def on_command_error(ctx, error):
    error_msg = f'Unhandled error occurred: {error}'
    if isinstance(error, commands.BadArgument):
        error_msg = 'I could not find that member...'
    await ctx.send(error_msg)

@tasks.loop(seconds=60)  # task runs every 60 seconds
async def reminder_task():
    # print(datetime.now())
    active = rem.get_active_reminders()
    send_reminders = {}
    for reminder in active:
        print(reminder)
        channel_id = reminder['channel']
        interval = reminder['interval']
        last_run = reminder['last_run']
        if last_run is None:
            if not channel_id in send_reminders:
                send_reminders[channel_id] = []
            send_reminders[channel_id].append(reminder)
        else:
            cur_time = time.time()
            if interval == "daily" and cur_time > (last_run + timedelta(days=1).total_seconds()):
                send_reminders[channel_id].append(reminder)
            elif interval == "weekly" and cur_time > (last_run + timedelta(weeks=1).total_seconds()):
                send_reminders[channel_id].append(reminder)
            elif interval == "monthly" and cur_time > (last_run + timedelta(months=1).total_seconds()):
                send_reminders[channel_id].append(reminder)


    for c, reminders in send_reminders.items():
        channel = await bot.fetch_channel(c)
        for r in reminders:
            await channel.send(f"{r['interval']} Reminder for {r['user']}!: {r['message']}")
            rem.update_last_run(r['id'])


# Run the command bot
bot.run(TOKEN)

