import discord
from discord.ext import commands
import requests
from task import TaskModel, TaskUpdate

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

@bot.command(name="h")
async def hello(ctx):
    command_list = ""
    command_list += "!employees\n"
    command_list += "!lookup <item name>\n"
    command_list += "!assign <task name (in quotes), employee_id. If task exists, task will reassign to emp_id\n"
    command_list += "!tasks <Optional: employee id>\n"
    command_list += "!complete <task id>"

    await ctx.send(command_list)

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

# --- Task Manager Commands ---
@bot.command(name="assign")
async def assign_task(ctx, task_name: str, employee_id: int):
    try:
        emp_response = requests.get(f"http://localhost:8000/employees/{employee_id}")
        if emp_response.status_code != 200:
            await ctx.send(f"❌ Employee ID {employee_id} not found.")
            return

        taskCheck = requests.get(f"http://localhost:8000/tasks/", params={'name': f'{task_name}'})
        tasks = taskCheck.json()

        if tasks:
            task_id = tasks[0].get('id', 'Unknown')
            task = TaskUpdate(employee_id=employee_id)
            task_response = requests.patch(f"http://localhost:8000/tasks/{task_id}", task.model_dump_json(exclude_unset=True))
            task_response.raise_for_status()

            await ctx.send(f"✅ Task re-assigned: {task_name} to employee #{employee_id}")

        else:
            task = TaskModel(id=1, name=task_name, employee_id=employee_id)

            task_response = requests.post(f"http://localhost:8000/tasks/", task.model_dump_json())
            task_response.raise_for_status()

            await ctx.send(f"✅ Task assigned: {task_name}")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {str(e)}")

@bot.command(name="tasks")
async def list_tasks(ctx, employee_id: int = None):
    try:
        response = requests.get("http://localhost:8000/tasks/")
        response.raise_for_status()
        tasks = response.json()
        if response.status_code != 200:
            await ctx.send("⚠️ Task system is unavailable.")
            return

        tasks = response.json()
        valid_tasks = []

        for task in tasks:
            emp_id = task.get("employee_id", "Unknown")
            if emp_id is None or not isinstance(emp_id, int):
                continue
            if employee_id is None or emp_id == employee_id:
                valid_tasks.append(task)

        if not valid_tasks:
            msg = f"No tasks found for employee {employee_id}" if employee_id else "No tasks available."
            await ctx.send(msg)
        else:
            reply = "\n".join(
                f"ID: {task['id']} | Task: {task['name']} | Employee: {task['employee_id']}"
                for task in valid_tasks
            )
            await ctx.send(f"**Tasks:**\n{reply}")

    except Exception as e:
        await ctx.send(f"❌ Error fetching tasks: {str(e)}")

@bot.command(name="complete")
async def complete_task(ctx, task_id: int):
    """Mark a task as completed by deleting it from the API backend"""
    try:
        # First check if the task exists
        check_response = requests.get(f"http://localhost:8000/tasks/{task_id}")
        if check_response.status_code != 200:
            await ctx.send(f"❌ Task ID {task_id} not found.")
            return

        # Proceed to delete the task
        delete_response = requests.delete(f"http://localhost:8000/tasks/{task_id}")
        if delete_response.status_code == 200:
            task_data = check_response.json()
            await ctx.send(f"✅ Completed: {task_data['name']} (ID: {task_id})")
        else:
            await ctx.send(f"⚠️ Failed to complete task {task_id}.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {str(e)}")

TOKEN = ''
bot.run(TOKEN)
