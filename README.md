# 7 Days of Legend

Everyone has their own flaws. Their patterns that they find themselves stuck in day after day, with no improvement or change in sight. I myself have found myself in this same situation. Occasionally, I will find myself filled with motivation to make a change, but it ends up only being short lived, sometimes not even lasting an entire day. I'll have plans to do something, but then find every excuse I can to delay doing it, until I decide that it's too late to do it so I'll just push it off. 
As you can tell, this isn't the greatest thing, being stuck in one position hardly moving forward at all.

However, it has reached the point where I can no longer afford to push the need for change aside. Something has to change... So I decided to make a program to help me along the way.

## About
So this will be a remake (about the 5th one, but this one is different... I guess) of my ScheduleKeeper, but with a different approach. Due to bursts of motivation of late, I've been able to start feeling excited about programming again, a feeling which was all but gone due to school and work. That's how I found myself here. This program will follow an idea I have had in my head for ages, but never got around to doing... that is... A Week of Change, or as I had it in my head, 7 Days of Legend. The idea behind it, is that if I am able to maintain the schedule for an entire week, with different tasks per day, and then maintain it for a month, it will eventually become a routine and I will be able to improve as an individual. The tasks themselves will be every self improvement thing that I can think of that I can do. It's all about pushing myself to evolve to the next stage.

## How it will work
### Note, this is how it will / should work. When I have actually finished it, I will change this to How it works.

Features
- Will use Text to Speech to state out schedule events when their time arrives. Planning to hook it up to my speaker so I can't miss it.
- ~~Will use Speech Recognition for remote control. Will keep this part simple to avoid errors with speech recognition software.~~
- Will use simple text files in a simple format to store the schedule for each day. This is to make modifications easy because as we all now, life isn't a straight line.
- Should be set as a task, so that whenever device is turned on, the script will start. Hardest part of a schedulekeeper is using it. This should help avoid that problem.
- Text files containing schedules will be stored using my FileServer, so that I can make necessary modifications and view it from any device in the house, including my phone.

## How it actually works
When the program is created for the first time, a folder named `schedules` will be created in the current directory, along with 8 files, one for each day of the week, and another one named daily.txt.
As can be expected, the ones for each day of the week, are for you to put your expected schedule inside of, following the provided format. For the daily.txt, any schedule that you would expect to follow on a day to day basis can be put here, following the same format. This daily schedule will be loaded along with the schedule for the current day. 

Note: If a set time exists in both the daily schedule and the schedule for the current day, the daily one will be overwritten. You will be notified of this clash when the schedule is loaded into the program.

To set schedules, as mentioned, simply go to the respective file located inside of the `schedules` folder, and add the time and tasks in the following format: time_in_24_hours: task

Example:
1. 600: Wake up.
2. 1300: get lunch.
3. 1800: Get dinner.

As should be expected, the program automatically keeps track of the time, and when a new day has come, the schedule for the appropiate day will be loaded into memory.

When the time for a given task arrives, you will be notified via a text to speech bot, of both the time, and the task to be done twice, in 40 second intervals.

Inside of the `config.yaml` file, there are some options that you can change up to customize how the program will behave.

## Using the created config.yaml file
Note: If you run the program from the main.exe application, the generated config.yaml file will not contain instructions, as such, they will be listed here.

folder_location: This is the location where the program will look into when finding your schedules.
text_to_speech: The three attributes in here will affect the text to speech program.
- rate: This is how fast the voice will speak text. Bigger number means faster speech
- voice: Whether the voice of the tts is male or female. 0 is for male, 1 is for female
- volume: How loud the voice should be. 1.0 is default, 0.0 is silent. 

## Extra
Originally, was supposed to just be a me thing, but I decided that since I was going to store it on Github anyway, might as well have it public, just in case it catches the eye of any of you.

I think that covers the basics of how I want it to work... now just implementing it!