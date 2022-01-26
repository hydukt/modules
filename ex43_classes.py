from sys import exit
from random import randint
from textwrap import dedent

class Scene(object):

    def enter(self):
        print("This scene is not yet configured.")
        print("Subclass it and implement enter().")
        exit(1)

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)
        
        current_scene.enter()

class Death(Scene):

        quips = [
            "You died. You kinda suck at this.",
            "Your Mom would be proud..if she were smarter."
        ]
        
        def enter(self):
            print(Death.quips[randint(0,len(self.quips)-1)])
            exit(1)

class CentralCorridor(Scene):
    def enter(self):
        print(dedent("""
                The Gothons of Planet Percal #25 have invaded your ship and destroyed
                your entire crew. Get to the bomb from the Weapons Armory, put it on
                the bridge and blow the ship up after getting into a pod.
                
                You run down the corridor, a Gorthon jumps out. He's blocking the
                door and about to pull a weapon.
                """))
        action = input("> ")

        if action == "shoot!":
            print(dedent("""
                  You fire at the Gothon, he eats you.
                  """))
            return 'death'
        
        elif action == "dodge!":
            print(dedent("""
                  You dodge and weave and slide right as the blaster cranks a laser
                  past your head. Your foot slops and you hit your head. You wake up to
                  the Gothon eating you.
                  """))
            return 'death'

        elif action == "tell a joke":
            print(dedent("""
                  You tell a joke to the Gothon in their native language. It bursts out
                  laughing and cannot move. You shoot him and jump through the door.
                  """))
            return 'laser_weapon_armory'

        else:
            print("Does not compute!")
            return 'central_corridor'


class LaserWeaponArmory(Scene):

    def enter(self):
        print(dedent("""
              You do a dive roll into the Weapon Armory, crouch and scan the room
              for more Gothons. You find the bomb in its container. There's a keypad
              lock on the box and you need the code to get the bomb. You have 10 tries,
               the code is 3 digits.
               """))

        code = f"{randint(1,9)}{randint(1,9)}{randint(1,9)}"
        guess = input("[keypad]> ")
        guesses = 1

        print(code)

        while guess != code and guesses < 10:
            print("BZZZZZED!")
            guesses += 1
            guess = input("[keypad]> ")
                
        if guess == code:
            print(dedent("""
                        The container clicks open and the seal breaks, letting
                        gas out. You grab the neutron bomb and run as fast as you can 
                        to the bridge where you must place it.
                        """))
            return 'the_bridge'
        else:
            print(dedent("""
                        The lock buzzes one last time and then you hear a
                        sickening meltng sound as the mechanism is fused
                        together. You blow up"""))
                        
        return 'death'

class TheBridge(Scene):

    def enter(self):
        print(dedent("""
              Youo burst onto the Bridge with the bomb in your arm
              and surprise the 5 Gothons who are trying to take control
              of the ship.
              """))

        action = input("> ")

        if action == "throw the bomb":
            print(dedent("""
                        In a panic you throw the bomb at the group of Gothons
                        and make a leap for the door. You're shot in the back
                        and die.
                         """))
            return 'death'
            
        elif action == "slowly place the bomb":
            print(dedent("""
                    You point your blaster at the bomb under your arm. You
                    inch backwards, open and place it. You then jump back
                    through the door and blast the lock, trapping the 
                    Gothons. You make way for the escape pod.
                    """))

            return 'escape_pod'
            
        else:
            print("DOES NOT COMPUTE!")
            return "the_bridge"
              
class EscapePod(Scene):

    def enter(self):
        print(dedent("""
                     You rush through the shit trying to find the escape pod.
                     You get to the chamber and need to pick one. There's 5
                     pods, which do you take
                     """))

        good_pod = randint(1, 5)
        guess = input("[pod #]> ")

        if int(guess) != good_pod:
            print(dedent(f"""
                         You jump into pod {guess} and hit the eject button.
                         The pod escapes out into the void of space, then
                         implodes as the hull ruptures, crushing your body
                         into jam jelly.
                         """))
            return 'death'

        else:
            print(dedent(f"""
                   You jump into pod {guess} and hit the eject button.
                   the pod easily slides out into space heading to the
                   planet below. You look back to see the ship explode, 
                   taking out the Gothon ship at the same time. You win!
                   """))

            return 'finished'

class Finished(Scene):

    def enter(self):
        print("You won! Good job.")
        return 'finished'

class Map(object):

    scenes = {
        'central_corridor': CentralCorridor(),
        'laser_weapon_armory': LaserWeaponArmory(),
        'the_bridge':  TheBridge(),
        'escape_pod': EscapePod(),
        'death': Death(),
        'finished': Finished()
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene
    
    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    def opening_scene(self):
        return self.next_scene(self.start_scene)

a_map = Map('central_corridor')
a_game = Engine(a_map)
a_game.play()

