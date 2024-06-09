from django.shortcuts import render, redirect
from .forms import CharacterForm, GameChoiceForm
from .models import Character_create, Stats
from .configure import adjust_stats

#logout
from django.contrib.auth import logout


from django.http import HttpResponse
import re
import openai
from openai import OpenAI

import os
from django.contrib.auth import authenticate, login
from .models import custom_user

from dotenv import load_dotenv

# Pinecone, vector database.
from pinecone import Pinecone, ServerlessSpec


pc = Pinecone(api_key='2c4fef42-7136-4fde-a0e0-db97ae1c775e')

messages = []

openai.api_key = "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"
client = OpenAI(api_key=openai.api_key)
model = "gpt-4"



def index(request):
    """The home page for CrossRoads"""
    return render(request, 'silk/index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Retrieve the password from POST data

        user = custom_user.objects.filter(username=username).first()
        if not user:
            # Create a new user if the user doesn't exist
            # Here, we also set the password for the user
            user = custom_user.objects.create_user(username=username, password=password)
        print("Attempting to authenticate user:", username)

        # Authenticate the user using both username and password
        user = authenticate(request, username=username, password=password)


        if user:
            # Create an Index for the user if authenticated.
            index_name = username

            pc.create_index(
                name=index_name,
                dimension=256,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )

            request.session['username'] = username
            # Create variables to use and update later
            i = 0
            request.session['i'] = i


            print("User authenticated. Logging in and redirecting.")
            login(request, user)
            return redirect('silk:story')  # Redirect to the input/index page after login
        else:
            print("User authentication failed.")
    return render(request, 'silk/index.html')


def custom_logout(request):
    # Retrieve the user's index name from the session
    username = request.session.get('username')
    print(username)
    if username:
        # Delete the index
        pc.delete_index(username)

    # Reset user stats...
    # Example: Resetting session stats
    #if 'stats' in request.session:
        #del request.session['stats']

    # Actual logout
    logout(request)
    #messages.info(request, "You have successfully logged out.")
    return redirect('silk:index')  # Redirect to login page or home page

def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            age = request.POST.get('age')
            ethnicity = request.POST.get('ethnicity')
            traits = request.POST.get('traits')
            background = request.POST.get('background')
            type_story = request.POST.get('type_story')
            personality = request.POST.get('personality')
            gender = request.POST.get('gender')
            year = request.POST.get('year')
            form.save()

            # Save the inputs into the session
            request.session['name'] = name
            request.session['age'] = age
            request.session['ethnicity'] = ethnicity
            request.session['traits'] = traits
            request.session['background'] = background
            request.session['type_story'] = type_story
            request.session['personality'] = personality
            request.session['gender'] = gender
            request.session['year'] = year

            # Make the adjustments based on the inputs the user did
            stats = adjust_stats(ethnicity, personality, traits)
            # Save the character changes
            character = form.save(commit=False)
            character.user = request.user
            character.save()

            # Fetch or create the stats for the character and update them
            character_stats, created = Stats.objects.get_or_create(user=character.user)
            character_stats.moral_compass += stats['moral_compass']
            character_stats.rizz += stats['rizz']
            character_stats.reputation += stats['reputation']
            character_stats.influence += stats['influence']
            character_stats.battery += stats['battery']
            character_stats.skills += stats['skills']
            character_stats.esteem += stats['esteem']
            character_stats.save()

            # name, age, gender, traits, background, type_story, personality
            users_character = Character_create(name, age, gender, background, type_story)

            # Construct the absolute path of the file and read from the file of the character background story example.
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'background_example.txt')
            with open(file_path, 'r') as f:
                example = f.read().replace('\n', ' ')

            # Just to create the attitude of the bot and generate a response
            response00 = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a descriptive real-life story creator. "},
                    {"role": "user",
                     "content": (f"Patricio a male, they are 20 years old, their background is: "
                                 f"(Mexican CS major studying in Bremen and in love with this girl called Emma), "
                                 f"write a short background story for this character by "
                                 f"crafting a realistic narrative that sets the tone for his Romance-oriented story."
                                 f" Keep it concise, no more than one paragraph.")},

                    {"role": "assistant", "content": f"{example}"},
                    {"role": "user", "content": f"{users_character}"}
                ]
            )
            response1 = response00.choices[0].message.content.replace('\n', '<br>')

            # Construct the absolute path of the file and read from the file of the world story example.
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world_example.txt')
            with open(file_path, 'r') as f:
                example1 = f.read().replace('\n', ' ')

            # Just to create the attitude of the bot and generate a response
            response01 = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a descriptive world story creator of a {type_story}-oriented story. "},
                    {"role": "user",
                     "content": f"describe the world and setting that the character Patricio would be living and interacting with, this is his background story "
                                f"(Mexican CS major studying in Bremen and in love with this girl called Emma)"
                                f"While saying a explicit location where they live, new persons of interest and specific challenges to overcome "
                                f"catering to his story as a extrovert and empath, so that the user"
                                f" has an idea of how his story could unfold. Make it concise, one/two paragraph long."},

                    {"role": "assistant", "content": f"{example1}"},
                    {"role": "user", "content": f"describe the world and setting that {name} would be living and interacting with, this is his background story ({response1}). "
                                                f"While saying a explicit location where they live, new persons of interest and specific challenges to overcome , so that the user"
                                                f" has an idea of how his story could unfold. Make it concise, one/two paragraph long."}
                ]
            )
            response2 = response01.choices[0].message.content.replace('\n', '<br>')

            response03 = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You summarize and return the core plots, sublots, core people, and core challenges of {name}s story in the shortest and most concise way possible. "},
                    {"role": "user",
                     "content": f"Patricio's story: {example} , Patricio's setting and people of interest: {example1} (response max 150 characters)"},

                    {"role": "assistant", "content": f"Central plot: Make Emma my girlfriend\nSubplots: pass CS exams, learn to live abroad\n"
                                                     f"People of Interest: Emma (girl that I am attracted to), Mark (newly made friend)\n"},
                    {"role": "user",
                     "content": f"{name}'s story: {response1}, {name}'s setting and people of interest: {response2}"},
                ]
            )
            response3 = response03.choices[0].message.content.replace('\n', '<br>')
            # Save the responses to the session
            request.session['character_story'] = response1
            request.session['world_story'] = response2
            request.session['plot_story'] = response3

            # Accessing the index created in the user function
            index_name = request.session.get('username')
            if index_name:
                index = pc.Index(index_name)



            character_traits = f"Name: {name}, Age: {age}, Gender: {gender}, Traits: {traits}, " \
                               f"Background: {background}, Type of Story: {type_story}, Personality: {personality}"

            # Make embeddings for the vector values
            MODEL = "text-embedding-3-large"

            embedding_traits = client.embeddings.create(input=[character_traits], model=MODEL, dimensions=256)
            embedding_cstory = client.embeddings.create(input=[response1], model=MODEL, dimensions=256)
            embedding_wstory = client.embeddings.create(input=[response2], model=MODEL, dimensions=256)

            # Accessing the embeddings from the response object
            vector_traits = embedding_traits.data[0].embedding
            vector_cstory = embedding_cstory.data[0].embedding
            vector_wstory = embedding_wstory.data[0].embedding

            # Assuming you have the embeddings stored in embedding_traits, embedding_cstory, embedding_wstory
            index.upsert(
                vectors=[
                {
                    "id": "character_traits",
                    "values": vector_traits,  # Replace `.vector` with the actual attribute if different
                    "metadata": {
                        "text": character_traits,
                        "document_name": "Character Traits Document"
                    }
                },
                {
                    "id": "character_story",
                    "values": vector_cstory,  # Adjust the attribute name as needed
                    "metadata": {
                        "text": response1,
                        "document_name": "Character Story Document"
                    }
                },
                {
                    "id": "world_story",
                    "values": vector_wstory,  # Adjust the attribute name as needed
                    "metadata": {
                        "text": response2,
                        "document_name": "World Story Document"
                    }
                }
            ]
        )

            return render(request, 'silk/story.html', {'response1': response1, 'response2': response2})
    else:
        form = CharacterForm()
    return render(request, 'silk/story.html', {'form': form})

def game_view(request):
    # Fetching character story, world story, and role from the session
    global location_time
    character_story = request.session.get('character_story', '')
    world_story = request.session.get('world_story', '')
    plot_story = request.session.get('plot_story', '')
    gender = request.session.get('gender', '')
    traits = request.session.get('traits', '')
    personality = request.session.get('personality', '')
    name = request.session.get('name', '')
    year = request.session.get('year', '')
    type_story = request.session.get('type_story','')

    if request.method == "POST":

        POST = True
        t = request.session.get('t')
        location_info = request.session.get('location_info', '')
        if t == 0:
            request.session['t'] = t + 1
        else:
            location_info = request.session.get('location_info', '')
            location_info = (f"given the location and date from the previous choice: {location_info} and how the story proceeds, write the changed contents of it."
                             "but maintain the exact same structure, that being: Location: (the location)), Date: (__.__.__), Time: (__:__)")


        selected_option = request.POST.get("choice")
        custom_option = request.POST.get("custom_choice")  # Get the custom choice from POST data

        if custom_option:
            # Here you will handle the custom choice. For now, let's just set selected_option to custom_option
            selected_option = custom_option
            request.session['choice'] = custom_option

        # Accessing the index we created in the user function
        index_name = request.session.get('username')
        if index_name:
            index = pc.Index(index_name)

        swc = request.session.get('story_without_choices')
        last_segment = f"{swc}\n They choose to do this next: {selected_option}"
        # For Fine-Tuning later.
        print(f"QUERY VECTOR SEGMENT: {last_segment}")

        MODEL = "text-embedding-3-large"
        embeddings = client.embeddings.create(input=[last_segment], model=MODEL, dimensions=256)
        vector = embeddings.data[0].embedding

        # Retrieve all documents with similarity based on the vector search
        result = index.query(
            vector= vector,
            top_k=2,
            include_metadata=True
        )

        # Change the raw results into a list of the data that we actually need
        contexts = []
        for res in result['matches']:
            contexts.append(f"{res['metadata']['text']}")

        augmented_query = "\n\n".join(contexts)
        past_segment = swc
        #print(f"\n\n\n{augmented_query}")

        # Make a way to see if 80-90% of the content of these both are similar. If so to remove augmented query.
        if past_segment == augmented_query:
            augmented_query = " "

        prompt_content = ( f"After this  past segment: ({past_segment}) {name} made the choice to: ({selected_option}), {name}'s core plot and people of interest are: {plot_story} "
                           f"YOUR JOB: write at the exactly: ({location_info}), then describe how {name}'s story progresses after this choice has been made. THE NEW SEGMENT CAN BE MAX 150 characters, NOT LONGER THAN 3 SENTENCES)"
                           f"Maintain a deliberate, slow pace as if in a choose-your-own-story game, use other past segments for context -> ({augmented_query})."
                            f"!!(IMPORTANT) Format the SHORT response with 'Choice 1:' and 'Choice 2:', each followed by the next choices '{name}' can make from the story progression you write (max 100 characters each).!!"
                           f"It could be a choice to answer a question of a dialogue, do an activity, call someone, sleep etc, dont make the decisions"
                           f"drastic if not necessary.\n"
                           f"End with 'Repercussions:', clearly listing the actual consequences of the choice made on the past segment (not the one hes about to make), if there is any, up to 3 repercussions."
                            f"Ensure your narrative is engaging and can include elements like comedy, romance, ethical dilemmas, or dialogue."
                            f"Focus on their whole life (work, school, uni, friends, love-interests, activities, hobbies, responsibilities, insecurities"
                           f"etc.) making him/her a complex character. Do not stay on the same subject for more than 3 prompts. Have multiple facets of their life."
                           f"Their story can deviate from the plot, but try to keep in mind every once in a while. \n"
                           "Ensure the story maintains continuity in location and interactions. "
                           "Avoid jumping between places or major narrative shifts without a transition."

                           )
        # For Fine-Tuning later
        print("\n\nPrompt Content:\n"+prompt_content)
        # For Fine Tuning later...
        #print(f"\n\n\nSYSTEM: \n\n Dion is a realistic, slow-paced, engaging, make-your-own-{type_story}-story game guide of "
              #f"{name} in the year: {year}. You display clear choices after writing the next segment of the story based on the "
             # f"last choice made. You react and create the next segment based on the stats, last segments, and information given.")

        #print(f"\n\n\nPROMPT CONTENT:"
                 # f"Past segment: {past_segment}\n"
               #   f"{name}'s past decision: '{selected_option}'\n"
                #  f"Related segments: {augmented_query}\n"
                #  f"Central Plots and people: {plot_story}\n"
                #  f"Stats: Energy (), Reputation () , Financial Stability (), Social Skills () , Anxiety ()\n"
                #  f"Location, date, and time: {location_info}\n"
                 # f"Next Segment (150 chars):\n"
                 # f"Craft the new segment using the above info. Ensure the segment follows the past story. Be engaging but realistic. Incorporate morality, romance, dilemmas, challenges, hardships, dialogue, and comedy accordingly. \n"
                 # f"Choice 1: (100 chars)\n"
                 # f"Choice 2: (100 chars)\n"
                 # f"Repercussions from past segment: (3 max)\n"
              # )

        messages= [
                {"role": "system",
                 "content": f"You are a creator of realistic, detailed narratives of a {type_story}-oriented story. "
                            f"The character {name} evolves as a person, making him a complex personality with a multifaceted story. "
                            f"Giving way to different choices now and then that differ from the central plot."
                            f"Craft stories that reflect how actions would realistically occur in the year {year}, "
                            "considering the social and cultural context of the characters involved."
                            " Ensure each segment is slow-paced, and ends with clear choices and repercussions."
                            
                            " Don't stay on a single topic for more that 2-3 prompts"},
                {
                "role": "user", "content": "After this  past segment: (As they stroll through the lamp-lit streets, Kevin braces against the evening chill, offering his jacket to Caro who smiles and wraps it around herself. The city's sounds become a backdrop as they share comfortable silences and light conversation. When they reach Caro's apartment building, Kevin finds himself not wanting the night to end.<br><br><br>Repercussions:<br>1. Offering his jacket; a tender act heightening the romantic undertone of their walk.<br>2. The atmosphere during the walk deepens their emotional connection.<br>3. Kevin's sense of not wanting the night to end indicates growing romantic feelings.) Kevin made the choice to: (lean in for a kiss), Kevin's core plot and people of interest are: Core Plot: Kevin attempts to transform his friendship with Caro into a romantic relationship.  <br>Subplots: Kevin's balancing act of expressing love without ruining the friendship, and his interactions with Maya, who advises him on his romantic pursuit.  <br>Core People: Kevin (protagonist in love), Caro (the friend he loves), Maya (Kevin's advisor and confidante).  <br>Core Challenges: Expressing his romantic feelings to Caro without jeopardizing their friendship. YOUR JOB: write at the top given the location and date from the previous choice: Location: Streets of the city, Date: 05.10.2024, Time: 21:00<br><br> and how the story proceeds, write the changed contents of it.but maintain its structure, that being: Location: ..., date: __.__.__, Time: __:__, then describe how Kevin's story progresses after this choice has been made. THE NEW SEGMENT CAN BE MAX 150 characters, NOT LONGER THAN 3 SENTENCES)Maintain a deliberate, slow pace as if in a choose-your-own-story game, use other past segments for context -> (Choice 3: The choice made: (Offer to walk Caro home.)," 
                        "This happened after the choice: (As they stroll through the lamp-lit streets, Kevin braces against the evening chill, offering his jacket to Caro who smiles and wraps it around herself. The city's sounds become a backdrop as they share comfortable silences and light conversation. When they reach Caro's apartment building, Kevin finds himself not wanting the night to end.<br><br><br>)"
                        "Choice 2: The choice made: (Suggest they grab dinner, just the two of them.), "
                        "This happened after the choice: (At a cozy corner table, Kevin and Caro indulge in a quiet dinner, the atmosphere intimate with soft music and dim lighting. The conversation drifts from class projects to personal aspirations, and Kevin finds himself listening more than speaking, captivated by Caro's passion and dreams. As they finish their meal, the waiter drops off the check, presenting a moment for Kevin to extend the evening.<br><br><br>)).!!(IMPORTANT) Format the SHORT response with 'Choice 1:' and 'Choice 2:', each followed by the next choices 'Kevin' can make from the story progression you write (max 100 characters each).!!It could be a choice to answer a question of a dialogue, do an activity, call someone, sleep etc, dont make the decisionsdrastic if not necessary."
                        "End with 'Repercussions:', clearly listing the actual consequences of the choice made on the past segment (not the one hes about to make), if there is any, up to 3 repercussions.Ensure your narrative is engaging and can include elements like comedy, romance, ethical dilemmas, or dialogue.Focus on their whole life (work, school, uni, friends, love-interests, activities, hobbies, responsibilities, insecuritiesetc.) making him/her a complex character. Do not stay on the same subject for more than 3 prompts. Have multiple facets of their life.Their story can deviate from the plot, but try to keep in mind every once in a while. "
                        "Ensure the story maintains continuity in location and interactions. Avoid jumping between places or major narrative shifts without a transition."},

            {"role": "assistant", "content": 'Front of Caro\'s apartment building, Date: 05.10.2024, Time: 21:05\n\nAs Kevin leans in, Caro hesitates briefly but then reciprocates his kiss. They break apart, a mix of smiles and surprise on their faces. Caro touches his cheek gently, "I didn\'t expect that."\n\nChoice 1: Invite Caro for a nightcap coffee.\nChoice 2: Respectfully say goodnight and plan another date.\n\nRepercussions:\n1. Kevin\'s act of kissing Caro changes their dynamic, possibly adding romantic tension.\n2. Caro\'s gentle touch and response may indicate mutual feelings.\n3. This moment can deepen their connection or create uncertainty about their friendship\'s future.'
            },
                # For Fine-Tuning purposes later.
                 #{"role": "user",
                 #"content": f"After making the choice 'ask for her number', describe how Patricio's story progresses (max 150 characters)"
                        #    f"Maintain a deliberate, slow pace as if in a choose-your-own-story game, you can use related segments '{augmented_query}' for context."
                         #   f"End with 'Repercussions:', clearly listing the actual consequences of the choice just made, if there is any, up to 3 repercussions."
                        #    f"Ensure your narrative is engaging and can include elements like comedy, romance, ethical dilemmas, or dialogue."
                        #    f"Focus on his life (work, school, uni, friends, love-interests, activities, hobbies, responsibilities, insecurities"
                        #   f"etc.) making him/her a complex character.\n"
                        #    f"!!(IMPORTANT) Format the response with 'Choice 1:' and 'Choice 2:', each followed by the next choices (max 100 characters each).!!\n"
                         #  f"It could be a choice of answer of a question of a dialogue someone asked, do an activity, call someone, sleep etc, dont make the decisions"
                        #   f"drastic if not necessary."},

               # {"role": "assistant", "content": f"{example1}"},

                {"role": "user", "content": prompt_content}
            ]


    else:
        POST = False
        prompt_content = (f"In a world where {world_story}, a {gender} named {name} begins their journey in the year {year}. "
                          f"He is an {personality}, that is a {traits}."
                          f"Write three/four sentences that encapsulates the start of a unique story, catered specifically for their story: {character_story}."
                          f"Do that in a sense that is engaging and concise ."
                          f"!!(IMPORTANT) Format the response with 'Choice 1:' and 'Choice 2:', each followed by the next choices '{name}' can make from the story progression you write (max 100 characters each).!!"
                         #f"You can use, comedy, romance, ethical dilemmas etc. For this desired effect."
                          )

                          #f"Guided by principles of rich storytelling like {story_making}, "
                          #f"ALWAYS present the current and only scenario followed by 'Choice 1:'linebreak  and 'Choice 2:'linebreak indicating two choices the player can make.  ")
        # Opening Files to use as examples for the AI.
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'background_example.txt')
        with open(file_path, 'r') as f:
            back_example = f.read().replace('\n', ' ')
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world_example.txt')
        with open(file_path, 'r') as f:
            world_example = f.read().replace('\n', ' ')
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'start_example.txt')
        with open(file_path, 'r') as f:
            start_example = f.read().replace('\n', ' ')

        messages = [
            {"role": "system",
             "content": f"You are tasked with crafting the opening segment of a {type_story}-oriented story. Start by describing a small, "
                        "yet significant moment or action involving the main character that hints at larger themes "
                        "or developments to come. Set the scene subtly and introduce characters in a way that feels "
                        "natural and intriguing, inviting readers to discover more about them as the story unfolds. "
                        "The opening should establish the mood and setting, setting the foundation for the narrative "
                        "that builds from this initial action."},
             {"role": "user",
             "content": f"In a world where {world_example}, a male named Patricio begins their journey in the year 2024. "
                          f"He is an extrovert, that is a visionary."
                          f"Write three/four sentences that encapsulates the start of a unique story, catered specifically for their story: {back_example}."
                          f"Do that in a sense that is engaging and concise ."
                         #f"You can use, comedy, romance, ethical dilemmas etc. For this desired effect."
                          f"Make it so that there is a choice to make, to start their story."
                          f"(IMPORTANT) Format the response with 'Choice 1:' and 'Choice 2:', each followed by the next choices (max 100 characters each)."
                          },

            {"role": "assistant", "content": f"{start_example}"},

            {"role": "user", "content": prompt_content}
        ]




    try:
        response = client.chat.completions.create(model=model, messages=messages)
        print(f"\n\nResponse:\n  {response}")
        next_segment = response.choices[0].message.content.replace('\n', '<br>')
        print(next_segment)
        # Remove Location, Date and Time from next_segment and save them in another variable.
        pattern = r"(Location.*?\n\n)"
        pattern2 = r"(Location.*?<br><br>)"
        location_info = re.search(pattern, next_segment, re.DOTALL)
        location_info2 = re.search(pattern2, next_segment, re.DOTALL)
        if location_info:
            location_info = location_info.group(0)
            request.session['location_info'] = location_info

            # Remove the substring from the original text
            next_segment = re.sub(pattern, "", next_segment, flags=re.DOTALL)
        elif location_info2:
            location_info = location_info2.group(0)
            request.session['location_info'] = location_info

            # Remove the substring from the original text
            next_segment = re.sub(pattern2, "", next_segment, flags=re.DOTALL)
        else:
            print("")

        next_segment = next_segment.replace("**","")

        if not POST:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'start_example.txt')
            with open(file_path, 'r') as f:
                start_example = f.read().replace('\n', ' ')
            location_time0 = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": f"You interpret from the story the location, and create a date and time to the story taking place"
                                f"in the year {year}."},
                    {"role": "user",
                     "content": f"story: {start_example} year: 2024"},
                    {"role": "assistant",
                     "content": f"Location: University, Date: 09.22.2024, Time: 13:30"},
                    {"role": "user",
                     "content": f"story: {next_segment} year: {year}"},
                ]
            )
            location_info = location_time0.choices[0].message.content.replace('\n', '<br>')
            t = 0
            request.session['t'] = t


        # Extract the choices from the next_segment
        choices = [choice[0] for choice in re.findall(r'Choice \d+: (.*?)(<br>|$)', next_segment)]

        # Remove the choices from the narrative for a cleaner presentation
        story_without_choices = re.sub(r'Choice \d+: .*?(<br>|$)', '', next_segment)
        choice_form = GameChoiceForm()

        # Save response to the session
        request.session['story_without_choices'] = story_without_choices

        # Fetch or create the user's stats
        stats, created = Stats.objects.get_or_create(user=request.user)

        if "Repercussions" in story_without_choices:
            # Find the position of the word "Repercussions"
            index = story_without_choices.index("Repercussions")

            # Extract the part of the string after the word "Repercussions"
            repercussions = story_without_choices[index:]

            # Modify the story_without_choices string to contain only what's before "Repercussions"
            story_without_choices = story_without_choices[:index]
        else:
            repercussions = ""

        # Accessing the index we created in the user function
        index_name = request.session.get('username')
        if index_name:
            index = pc.Index(index_name)

        i = request.session.get('i')

        #Make a joint string  on the part of the story and the selected option
        swc = story_without_choices
        select_option = request.POST.get("choice")
        last_segment = f"The choice made: ({select_option}), \nThis happened after the choice: ({swc})"

        # Generate an Embedding to use as vector values for the document that will be saved.
        MODEL = "text-embedding-3-large"
        embeddings2 = client.embeddings.create(input=[last_segment], model=MODEL, dimensions=256)
        vector2 = embeddings2.data[0].embedding
        index.upsert(
            vectors=[
                {
                    "id": f"Choice {i}",
                    "values": vector2,  # Replace `.vector` with the actual attribute if different
                    "metadata": {
                        "text": f"Choice {i}: {last_segment}",
                        #"location, date and time": location_time
                        #"document_name": f"Choice {i}"
                    }
                }])

        # Increment the number of choice the user is on.
        request.session['i'] = i + 1

        context = {
            'next_segment': story_without_choices,
            'choices': choices,
            'choice_form': choice_form,
            'stats': stats,
            'repercussions': repercussions,
            'plot': plot_story,
            'location_info': location_info,
            }

        return render(request, 'silk/game.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
