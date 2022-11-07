import asyncio
import importlib.resources as resources


async def say(line):
    with resources.as_file(resources.files(__package__)) as pth:
        proc = await asyncio.create_subprocess_exec(
            str(pth / 'bin' / 'mimic.exe'),
            "-t",
            line,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()


asyncio.run(say("why you run?! Argh!"))
