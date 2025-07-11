# chatbot_engine.py

import random
import json
import os

def get_devotion(topic):
    with open("content/devotionals.json", "r") as f:
        devotions = json.load(f)
    return devotions.get(topic, {
        "scripture": "Romans 8:28",
        "verse": "All things work together for good to those who love God.",
        "prayer": "Lord, I trust You in all circumstances.",
        "declaration": "God is working everything out for my good.",
        "video_url": "https://www.youtube.com/watch?v=default"
    })

def get_devotion(topic):
    content = {
        "Dealing with Stress": {
            "scripture": "Philippians 4:6-7",
            "prayer": "Lord, help me release my anxieties and trust in You.",
            "declaration": "God is my refuge, and I will not be shaken.",
            "video": "Overcoming Fear with God’s Promises"
        },
        "Overcoming Fear": {
            "scripture": "Isaiah 41:10",
            "prayer": "God, remove fear from my heart and fill me with courage.",
            "declaration": "I am strong and courageous.",
            "video": "Facing Fear through Faith"
        }
    }
    return content.get(topic, random.choice(list(content.values())))

def get_prayer(topic):
    return {
        "adoration": "You are holy and worthy, Lord.",
        "confession": "I confess my sins and ask for your forgiveness.",
        "thanksgiving": "Thank You for Your endless grace.",
        "supplication": f"Please help me with {topic}."
    }

def get_meditation(topic):
    return {
        "scripture": "Psalm 46:10",
        "prompt": "Be still and know that I am God.",
        "reflection": f"How does '{topic}' reveal God’s nature?",
        "breathing": "Inhale 4s → Hold 4s → Exhale 4s"
    }

def get_accountability(area):
    return {
        "scripture": "Romans 6:14",
        "truth": "I am not a slave to temptation; I am free in Christ.",
        "action": f"Instead of {area}, try journaling or taking a walk.",
        "sos": "Click here to message a mentor or pray."
    }
