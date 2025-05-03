import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#This just makes sure that the user is the same and the bot doesnt respond to it's own message
def validateUser(message):
    return(
        message.author == ctx.author
        and message.channel == ctx.author
    )

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello")

@bot.command(name="employees")
async def employees(ctx):
    try:
        response = requests.get("http://localhost:8000/employees/")
        response.raise_for_status()
        employees = response.json()

        if not employees:
            await ctx.send("No employees found")
        else:
            names = [emp.get("name", "Unknown") for emp in employees]
            reply = "Employees:\n" + "\n".join(f"- {name}" for name in names)
            await ctx.send(reply)
          
    except requests.RequestException as e:
            await ctx.send(f"Failed to get employee(s):\n{e}")

@bot.command(name="lookup")
async def lookup(ctx, *, item_name: str):
    reply = ""
    try:
        response = requests.get("http://localhost:8000/items/", params={"name": item_name})
        response.raise_for_status()
        items = response.json()

        if not items:
            await ctx.send(f"No `{item_name}`(s) found")
            return
        else:
            for item in items:
                name = item.get("name", "Unknown")
                count = item.get("count", "Unknown")
                sold = item.get("sold_since_restock", "Unknown")
                reply += f"- **{name}** | In Stock: `{count}` | Sold Since Restock: `{sold}`\n"

            await ctx.send(reply)
                
    except requests.RequestException as e:
        await ctx.send(f"Failed to get Item(s):\n{e}")

#--- Task Manager Commands---
@bot.command(name="assign")
async def assign_task(ctx, task_name: str, employee_id: int):
    """Assign a new task to an employee. Usage: `!assign "Task Name" 1`"""
    try:
        response = requests.post(
            "http://localhost:8000/tasks/",
            json={"name": task_name, "employee_id": employee_id}
        )
        response.raise_for_status()
        await ctx.send(f" Task assigned to employee ID `{employee_id}`: *{task_name}*")
    except requests.RequestException as e:
        await ctx.send(f" Failed to assign task: `{e}`")

@bot.command(name="tasks")
async def list_tasks(ctx, employee_id: int = None):
    """List all tasks or filter by employee. Usage: `!tasks` or `!tasks 1`"""
    try:
        params = {"employee_id": employee_id} if employee_id else None
        response = requests.get("http://localhost:8000/tasks/", params=params)
        response.raise_for_status()
        tasks = response.json()

        if not tasks:
            await ctx.send("No tasks found.")
        else:
            task_list = "\n".join(
                f"**ID:** {t['id']} | **Task:** {t['name']} | **Assigned to:** {t['employee_id']}"
                for t in tasks
            )
            await ctx.send(f" **Tasks:**\n{task_list}")
    except requests.RequestException as e:
        await ctx.send(f" Failed to fetch tasks: `{e}`")

@bot.command(name="complete")
async def complete_task(ctx, task_id: int):
    """Mark a task as complete (deletes it). Usage: `!complete 1`"""
    try:
        response = requests.delete(f"http://localhost:8000/tasks/{task_id}")
        response.raise_for_status()
        await ctx.send(f" Task ID `{task_id}` marked as complete.")
    except requests.RequestException as e:
        await ctx.send(f" Failed to complete task: `{e}`")

TOKEN = ''
bot.run(TOKEN)
