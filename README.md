Alluvian Mud Engine
======

This repository contains the source code for the mud engine that powers Alluvian.  This mud engine is
heavily inspired by [Circlemud/Tbamud](https://tbamud.org) and is a fork of [mud-pi](https://github.com/Frimkron/mud-pi)
developed by Mark Frimston.  Mud-pi is a bare-bones mud server written in python.

Additional inspiration credits go to [Evennia](https://github.com/evennia/evennia).


Requirements
------------
* Virtualenv
* Python 3.8

Getting Started
--------------
1. Navigate to project root
2. Create a virtual-environment with python3.8 `virtualenv -p python3.8 venv`
3. Activate your virtualenv: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Load world into db: `python manage.py loaddata lib/world/rooms.json`
7. Run the mudserver: `python alluvian/server/alluvian.py`  (You will need to make sure that the `alluvian` folder is part of your python path)



What is a MUD?
--------------

MUD is short for Multi-User Dungeon. A MUD is a text-based online role-playing
game. MUDs were popular in the early 80s and were the precursor to the 
graphical Massively-Multiplayer Online Role-Playing Games we have today, like 
World of Warcraft. <http://www.mudconnect.com> is a great site for learning 
more about MUDs.
