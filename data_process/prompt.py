############ GQA ############

GQA_CURATED_EXAMPLES=[
"""Question: Is the vehicle in the top of the image?
Program:
BOX0=LOC(image=IMAGE,object='TOP')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='vehicle')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Are there trains or fences in this scene?
Program:
BOX0=LOC(image=IMAGE,object='train')
BOX1=LOC(image=IMAGE,object='fence')
ANSWER0=COUNT(box=BOX0)
ANSWER1=COUNT(box=BOX1)
ANSWER2=EVAL(expr="'yes' if {ANSWER0} + {ANSWER1} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER)
""",
"""Question: Who is carrying the umbrella?
Program:
ANSWER0=VQA(image=IMAGE,question='Who is carrying the umbrella?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Which place is it?
Program:
ANSWER0=VQA(image=IMAGE,question='Which place is it?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: What color is the curtain that is to the right of the mirror?
Program:
BOX0=LOC(image=IMAGE,object='mirror')
IMAGE0=CROP_RIGHTOF(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='What color is the curtain?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Is the pillow in the top part or in the bottom of the picture?
Program:
BOX0=LOC(image=IMAGE,object='TOP')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='pillow')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'top' if {ANSWER0} > 0 else 'bottom'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Question: Do you see bottles to the right of the wine on the left of the picture?
Program:
BOX0=LOC(image=IMAGE,object='LEFT')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='wine')
IMAGE1=CROP_RIGHTOF(image=IMAGE0,box=BOX1)
BOX2=LOC(image=IMAGE1,object='bottles')
ANSWER0=COUNT(box=BOX2)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Is the street light standing behind a truck?
Program:
BOX0=LOC(image=IMAGE,object='truck')
IMAGE0=CROP_BEHIND(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='street light')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Which side is the food on?
Program:
BOX0=LOC(image=IMAGE,object='RIGHT')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='food')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'right' if {ANSWER0} > 0 else 'left'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: What do the wetsuit and the sky have in common?
Program:
ANSWER0=VQA(image=IMAGE,question='What do the wetsuit and the sky have in common?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Do the post and the sign have a different colors?
Program:
BOX0=LOC(image=IMAGE,object='post')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='sign')
IMAGE1=CROP(image=IMAGE,box=BOX1)
ANSWER0=VQA(image=IMAGE0,question='What color is the post?')
ANSWER1=VQA(image=IMAGE1,question='What color is the sign?')
ANSWER2=EVAL(expr="'yes' if {ANSWER0} != {ANSWER1} else 'no'")
FINAL_RESULT=RESULT(var=ANSWER2)
""",
"""Question: Does the traffic cone have white color?
Program:
BOX0=LOC(image=IMAGE,object='traffic cone')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Does the traffic cone have white color?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Are these animals of different species?
Program:
ANSWER0=VQA(image=IMAGE,question='Are these animals of different species?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Which side of the image is the chair on?
Program:
BOX0=LOC(image=IMAGE,object='RIGHT')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='chair')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'right' if {ANSWER0} > 0 else 'left'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Do you see any drawers to the left of the plate?
Program:
BOX0=LOC(image=IMAGE,object='plate')
IMAGE0=CROP_LEFTOF(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='drawers')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Does the mat have the same color as the sky?
Program:
BOX0=LOC(image=IMAGE,object='sky')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='mat')
IMAGE1=CROP(image=IMAGE,box=BOX1)
ANSWER0=VQA(image=IMAGE0,question='What color is the sky?')
ANSWER1=VQA(image=IMAGE1,question='What color is the mat?')
ANSWER2=EVAL(expr="'yes' if {ANSWER0} == {ANSWER1} else 'no'")
FINAL_RESULT=RESULT(var=ANSWER2)
""",
"""Question: Is a cat above the mat?
Program:
BOX0=LOC(image=IMAGE,object='mat')
IMAGE0=CROP_ABOVE(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='cat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
"""
"""Question: Is the cat above a mat?
Program:
BOX0=LOC(image=IMAGE,object='cat')
IMAGE0=CROP_BELOW(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='mat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 and else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Is a mat near/next to/beside the cat?
Program:
BOX0=LOC(image=IMAGE,object='cat')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='mat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 and else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Which color does the mirror that is made of metal have?
Program:
BOX0=LOC(image=IMAGE,object='mirror')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Which color does the mirror that is made of metal have?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
]

GQA_MODULES_PROMPT = \
"""You can only use these modules in the program:
BOX=LOC(image=IMAGE,object='object')
ANSWER=COUNT(box=BOX)
IMAGE=CROP(image=IMAGE,box=BOX)
IMAGE=CROP_RIGHTOF(image=IMAGE,box=BOX)
IMAGE=CROP_LEFTOF(image=IMAGE,box=BOX)
IMAGE=CROP_INFRONTOF(image=IMAGE,box=BOX)
IMAGE=CROP_BEHIND(image=IMAGE,box=BOX)
IMAGE=CROP_BELOW(image=IMAGE,box=BOX)
IMAGE=CROP_ABOVE(image=IMAGE,box=BOX)
ANSWER=VQA(image=IMAGE,question='question')
ANSWER=EVAL(expr="expr")
FINAL_RESULT=RESULT(var=ANSWER)
Do not use any other modules!"""

def create_gqa_prompt(question):
    prompt_examples = '\n'.join(GQA_CURATED_EXAMPLES)
    prompt_examples = f'Give the visual program to solve the problem. Only output the program. Do not output ```.\n\n{GQA_MODULES_PROMPT}\n\n{prompt_examples}'
    return prompt_examples + f"\nQuestion: {question}\nProgram:"


############ NLVR ############

NLVR_CURATED_EXAMPLES=[
"""Statement: An image shows one bare hand with the thumb on the right holding up a belly-first, head-up crab, with water in the background.
Program:
ANSWER0=VQA(image=LEFT,question='Does the image shows one bare hand with the thumb on the right holding a crab?')
ANSWER1=VQA(image=RIGHT,question='Does the image shows one bare hand with the thumb on the right holding a crab?')
ANSWER2=VQA(image=LEFT,question='Is the crab belly-first and head-ups?')
ANSWER3=VQA(image=RIGHT,question='Is the crab belly-first and head-ups?')
ANSWER4=VQA(image=LEFT,question='Is there water in the background?')
ANSWER5=VQA(image=RIGHT,question='Is there water in the background?')
ANSWER6=EVAL(expr='{ANSWER0} and {ANSWER2} and {ANSWER4}')
ANSWER7=EVAL(expr='{ANSWER1} and {ANSWER3} and {ANSWER5}')
ANSWER8=EVAL(expr='{ANSWER6} xor {ANSWER7}')
FINAL_ANSWER=RESULT(var=ANSWER8)
""",
"""Statement: There is a red convertible in one image.
Program:
ANSWER0=VQA(image=LEFT,question='Is there a red convertible in the image?')
ANSWER1=VQA(image=RIGHT,question='Is there a red convertible in the image?')
ANSWER2=EVAL(expr='{ANSWER0} xor {ANSWER1}')
FINAL_ANSWER=RESULT(var=ANSWER2)
""",
"""Statement: One dog is laying down.
Program:
ANSWER0=VQA(image=LEFT,question='How many dogs are laying down?')
ANSWER1=VQA(image=RIGHT,question='How many dogs are laying down?')
ANSWER2=EVAL(expr='{ANSWER0} + {ANSWER1} == 1')
FINAL_ANSWER=RESULT(var=ANSWER2)
""",
"""Statement: There are two blue and yellow birds
Program:
ANSWER0=VQA(image=LEFT,question='How many blue and yellow birds are in the image?')
ANSWER1=VQA(image=RIGHT,question='How many blue and yellow birds are in the image?')
ANSWER2=EVAL(expr='{ANSWER0} + {ANSWER1} == 2')
FINAL_ANSWER=RESULT(var=ANSWER2)
""",
"""Statement: A single wolf is howling and silhouetted by the moon in one of the images.
Program:
ANSWER0=VQA(image=LEFT,question='How many wolves are in the image?')
ANSWER1=VQA(image=RIGHT,question='How many wolves are in the image?')
ANSWER2=VQA(image=LEFT,question='Is the wolf howling and silhouetted by the moon?')
ANSWER3=VQA(image=RIGHT,question='Is the wolf howling and silhouetted by the moon?')
ANSWER4=EVAL(expr='{ANSWER0} == 1 and {ANSWER2}')
ANSWER5=EVAL(expr='{ANSWER1} == 1 and {ANSWER3}')
ANSWER6=EVAL(expr='{ANSWER4} xor {ANSWER5}')
FINAL_ANSWER=RESULT(var=ANSWER6)
""",
"""Statement: One of the two images has a bag with the characters from Disney's Frozen on it.
Program:
ANSWER0=VQA(image=LEFT,question='Does the image have a bag with the characters from Disney's Frozen on it?')
ANSWER1=VQA(Image=RIGHT,question='Does the image have a bag with the characters from Disney's Frozen on it?')
ANSWER2=EVAL(expr='{ANSWER0} xor {ANSWER1}')
FINAL_ANSWER=RESULT(var=ANSWER2)
""",
"""Statement: there are at least seven wine bottles in the image on the left
Program:
ANSWER0=VQA(image=LEFT,question='How many wine bottles are in the image?')
ANSWER1=EVAL(expr='{ANSWER0} >= 7')
FINAL_ANSWER=RESULT(var=ANSWER1)
""",
"""Statement: An image shows broccoli growing in soil, with leaves surrounding the florets.
Program:
ANSWER0=VQA(image=LEFT,question='Does the image show broccoli growing in soil?')
ANSWER1=VQA(image=RIGHT,question='Does the image show broccoli growing in soil?')
ANSWER2=VQA(image=LEFT,question='Are leaves surrounding the floret?')
ANSWER3=VQA(image=RIGHT,question='Are leaves surrounding the floret?')
ANSWER4=EVAL(expr='{ANSWER0} and {ANSWER2}')
ANSWER5=EVAL(expr='{ANSWER1} and {ANSWER3}')
ANSWER6=EVAL(expr='{ANSWER4} xor {ANSWER5}')
FINAL_ANSWER=RESULT(var=ANSWER6)
""",
"""Statement: An image shows exactly two seals in direct contact, posed face to face.
Program:
ANSWER0=VQA(image=LEFT,question='How many seals are in the image?')
ANSWER1=VQA(image=RIGHT,question='How many seals are in the image?')
ANSWER2=VQA(image=LEFT,question='Are the seals in direct contact?')
ANSWER3=VQA(image=RIGHT,question='Are the seals in direct contact?')
ANSWER4=VQA(image=LEFT,question='Are the seals posed face to face?')
ANSWER5=VQA(image=RIGHT,question='Are the seals posed face to face?')
ANSWER6=EVAL(expr='{ANSWER0} == 2 and {ANSWER2} and {ANSWER4}')
ANSWER7=EVAL(expr='{ANSWER1} == 2 and {ANSWER3} and {ANSWER5}')
ANSWER8=EVAL(expr='{ANSWER6} xor {ANSWER7}')
FINAL_ANSWER=RESULT(var=ANSWER8)
""",
"""Statement: There is at least two parrots in the right image.
Program:
ANSWER0=VQA(image=RIGHT,question='How many parrots are in the image?')
ANSWER1=EVAL(expr='{ANSWER0} >= 2')
FINAL_ANSWER=RESULT(var=ANSWER1)
""",
"""Statement: In the image on the right, four people are riding in one canoe.
Program:
ANSWER0=VQA(image=RIGHT,question='Are there four people riding in one canoe?')
ANSWER1=EVAL(expr='{ANSWER0}')
FINAL_ANSWER=RESULT(var=ANSWER1)
""",
"""Statement: There are two wolves in each image.
Program:
ANSWER0=VQA(image=LEFT,question='How many wolves are in the image?')
ANSWER1=VQA(image=RIGHT,question='How many wolves are in the image?')
ANSWER2=EVAL(expr='{ANSWER0} == 2 and {ANSWER1} == 2')
FINAL_ANSWER=RESULT(var=ANSWER2)
"""
]

NLVR_MODULES_PROMPT = \
"""You can only use these modules in the program:
ANSWER=VQA(image=IMAGE,question='question')
ANSWER=EVAL(expr="expr")
FINAL_RESULT=RESULT(var=ANSWER)
Do not use any other modules!"""

def create_nlvr_prompt(statement):
    prompt_examples = '\n'.join(NLVR_CURATED_EXAMPLES)
    prompt_examples = f'Give the visual program to determine whether the statement is True or False. Only output the program. Do not output ```. Unless otherwise specified, the statement describes the combined situation in both images.\n\n{NLVR_MODULES_PROMPT}\n\n{prompt_examples}'
    return prompt_examples + f"\nStatement: {statement}\nProgram:"


############ Open Images ############

OPENIMAGES_CURATED_EXAMPLES=[
"""Question: What the mug contain?
Program:
ANSWER0=VQA(image=IMAGE,question='What the mug contain?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Where the chair is at?
Program:
ANSWER0=VQA(image=IMAGE,question='Where the chair is at?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",

"""Question: What the walking man plays?
Program:
ANSWER0=VQA(image=IMAGE,question='What the walking man plays?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: What the standing man wears?
Program:
BOX0=LOC(image=IMAGE,object='standing man')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='What the man wears?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Where the standing boy is at?
Program:
BOX0=LOC(image=IMAGE,object='standing boy')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Where the standing boy is at?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Who is at the wooden table?
Program:
ANSWER0=VQA(image=IMAGE,question='Who is at the wooden table?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Where the sitting man is on?
Program:
ANSWER0=VQA(image=IMAGE,question='Where the sitting man is on?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: What the smiling man ride?
Program:
BOX0=LOC(image=IMAGE,object='smiling man')
IMAGE0=CROP_BELOW(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='What the smiling man ride?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Who wears the cowboy hat?
Program:
ANSWER0=VQA(image=IMAGE,question='Who wears the cowboy hat?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Where the standing boy is under?
Program:
BOX0=LOC(image=IMAGE,object='standing boy')
IMAGE0=CROP_ABOVE(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Where the standing boy is under?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Who is on the plastic chair?
Program:
ANSWER0=VQA(image=IMAGE,question='Who is on the plastic chair?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: What material is the object that is at the wooden table made of?
Program:
BOX0=LOC(image=IMAGE,object='wooden table')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='object')
IMAGE1=CROP(image=IMAGE0,box=BOX1)
ANSWER0=VQA(image=IMAGE1,question='Is the object at the wooden table?')
ANSWER1=VQA(image=IMAGE1,question='What material is the object made of?')
ANSWER2=VQA(image=IMAGE,question='What material is the object that is at the wooden table made of?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
""",
"""Question: What material is the object that the standing woman is at made of?
Program:
BOX0=LOC(image=IMAGE,object='standing woman')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='object')
IMAGE1=CROP(image=IMAGE0,box=BOX1)
ANSWER0=VQA(image=IMAGE1,question='Is the object at the standing woman?')
ANSWER1=VQA(image=IMAGE1,question='What material is the object made of?')
ANSWER2=VQA(image=IMAGE,question='What material is the object that the standing woman is at made of?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
""",
"""Question: What is the people that wears the glasses doing?
Program:
BOX0=LOC(image=IMAGE,object='people')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Is this person wearing glasses?')
ANSWER1=VQA(image=IMAGE0,question='What is the people doing?')
ANSWER2=VQA(image=IMAGE,question='What is the people that wears the glasses doing?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
""",
"""Question: What is the people that wears the football helmet doing?
Program:
BOX0=LOC(image=IMAGE,object='people')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Is this person wearing a football helmet?')
ANSWER1=VQA(image=IMAGE0,question='What is the people doing?')
ANSWER2=VQA(image=IMAGE,question='What is the people that wears the football helmet doing?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
""",
"""Question: What is the people that holds the table tennis racket doing?
Program:
BOX0=LOC(image=IMAGE,object='people')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Is this person holding a table tennis racket?')
ANSWER1=VQA(image=IMAGE0,question='What is the people doing?')
ANSWER2=VQA(image=IMAGE,question='What is the people that holds the table tennis racket doing?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
""",
"""Question: What is the people that holds the guitar doing?
Program:
BOX0=LOC(image=IMAGE,object='people')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Is this person holding a guitar?')
ANSWER1=VQA(image=IMAGE0,question='What is the people doing?')
ANSWER2=VQA(image=IMAGE,question='What is the people that holds the guitar doing?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
""",
"""Question: What is the people that is under the tent doing?
Program:
BOX0=LOC(image=IMAGE,object='tent')
IMAGE0=CROP_BELOW(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='people')
IMAGE1=CROP(image=IMAGE0,box=BOX1)
ANSWER0=VQA(image=IMAGE1,question='What is the people doing?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: What is the people that the standing woman dance doing?
Program:
BOX0=LOC(image=IMAGE,object='people')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Is the people dancing with the standing woman?')
ANSWER1=VQA(image=IMAGE0,question='What is the people doing?')
ANSWER2=VQA(image=IMAGE,question='What is the people that the standing woman dance doing?')
ANSWER3=EVAL(expr="{ANSWER1} if {ANSWER0} == 'yes' else {ANSWER2}")
FINAL_RESULT=RESULT(var=ANSWER3)
"""
]

OPEN_IMAGES_MODULES_PROMPT = \
"""You can only use these modules in the program:
BOX=LOC(image=IMAGE,object='object')
ANSWER=COUNT(box=BOX)
IMAGE=CROP(image=IMAGE,box=BOX)
IMAGE=CROP_RIGHTOF(image=IMAGE,box=BOX)
IMAGE=CROP_LEFTOF(image=IMAGE,box=BOX)
IMAGE=CROP_INFRONTOF(image=IMAGE,box=BOX)
IMAGE=CROP_BEHIND(image=IMAGE,box=BOX)
IMAGE=CROP_BELOW(image=IMAGE,box=BOX)
IMAGE=CROP_ABOVE(image=IMAGE,box=BOX)
ANSWER=VQA(image=IMAGE,question='question')
ANSWER=EVAL(expr="expr")
FINAL_RESULT=RESULT(var=ANSWER)
IF(ANSWER=='yes'):ANSWER1=VQA(image=IMAGE,question='question')
ELSE:ANSWER1=VQA(image=IMAGE,question='question')
Do not use any other modules!"""

def create_open_images_prompt(inputs):
    prompt_examples = '\n'.join(OPENIMAGES_CURATED_EXAMPLES)
    prompt_examples = f'Give the visual program to solve the problem. Only output the program. Do not output ```.\n\n{OPEN_IMAGES_MODULES_PROMPT}\n\n{prompt_examples}'
    return prompt_examples + "\nQuestion: {question}\nProgram:".format(**inputs)