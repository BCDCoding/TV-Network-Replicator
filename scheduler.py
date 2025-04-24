import random
import os
global movieCounter
movieCounter = 9
showsPath = "../Media/Shows/"
commPath = "../Media/Commericals/"
moviePath = "../Media/Movies/"
upPath = "../Media/UpNext/"
bumpPath = "../Media/Bumpers/"
showList = os.listdir("../Media/Shows/")

def initalizer():
    rotationList = {}
    print(showList)
    lineUp = []
    syn = False
    ranIn = False
    ranCre = False
    index = 1
    for folder in showList:
        episodeList = os.listdir(showsPath + str(folder))
        test = {folder: episodeList}
        rotationList.update(test)

    schedule = random.choices(list(rotationList.keys()), k=9)
    for show in schedule:
        chosenEpisode, syn, ranIn, ranCre = episodeGrabber(rotationList, show)
        print(show + " :", chosenEpisode, ":", syn)
        lineUp = blockGenerator(chosenEpisode, syn, schedule, lineUp, show, ranIn, ranCre)
    return lineUp



def blockGenerator(episode, syndication, order, playlist, title, randIntr, randCred):
    global movieCounter
    intro = True
    upNextCount = 0
    for segment in episode:
        if upNextCount == len(episode) - 1:
            playlist = commercialInserter(playlist, 2, 3)
            try:
                nextShow = order[order.index(title) + 1]
                playlist.append(upPath + nextShow + ".mp4")
            except IndexError:
                playlist.append(upPath + title + ".mp4")
            playlist = commercialInserter(playlist, 3, 5)
        else:
            playlist = commercialInserter(playlist)
            playlist.append("../Media/BackTo/" + random.choice(os.listdir("../Media/BackTo/")))
        if syndication and intro:
            intro = False
            if episode.index(segment) != 0:
                playlist.append("../Media/BackTo/" + random.choice(os.listdir("../Media/BackTo/")))
            if randIntr:
                playlist.append(showsPath + title + "/" + random.choice(
                    [intro for intro in os.listdir(showsPath + title) if "INTRO" in intro]))
            else:
                playlist.append(showsPath + title + "/INTRO.mp4")

        playlist.append(showsPath + title + "/" + segment)
        if randCred and episode.index(segment) == len(episode) - 1:
            playlist.append(showsPath + title + "/" + random.choice(
                [credit for credit in os.listdir(showsPath + title) if "CREDIT" in credit]))
        playlist.append("../Media/ComBreak/" + random.choice(os.listdir("../Media/ComBreak/")))
        upNextCount += 1
    movieCounter -= 1

    if movieCounter <= 0:
        movieCounter = 15
        playlist = movieInserter(playlist)
    return playlist


def episodeGrabber(catalog, showTitle):
    holder = []
    randomIntro = False
    randomCredits = False

    if "INTRO.mp4" in catalog[showTitle]:
        startList = catalog[showTitle].copy()
        startList.remove("INTRO.mp4")
        syndicated = True

    elif any("INTRO" in segment for segment in catalog[showTitle]):
        startList = catalog[showTitle].copy()

        removeList = [end for end in startList if any(seg in end for seg in ["INTRO", "CREDIT"])]
        startList = [seg for seg in startList if seg not in removeList]
        syndicated = True
        randomIntro = True
        randomCredits = True

    else:
        startList = [episode for episode in catalog[showTitle] if episode.endswith("A.mp4")]
        syndicated = False

    if syndicated:
        holder = list(random.choices(startList, k=2))
    else:
        pickedEpisode = random.choice(startList)
        joiner = str((startList.index(pickedEpisode) + 1))
        for episode in catalog[showTitle]:
            if str(joiner) in episode.split('.')[0]:
                if joiner == '1' and '10' not in episode:
                    holder.append(episode)
                elif joiner != '1':
                    holder.append(episode)

    return holder, syndicated, randomIntro, randomCredits


def commercialInserter(playlist, low=4, high=6):
    insertBumper = random.randint(0, 1)
    checker = True
    counter = 0
    for commerical in random.choices(os.listdir(commPath), k=random.randint(low, high - 1)):
        playlist.append(commPath + commerical)
        counter += 1
        if insertBumper == 1 and checker and counter == 2:
            playlist.append(bumpPath + random.choice(os.listdir(bumpPath)))
            checker = False
    for commerical in random.choices(os.listdir(commPath), k=random.randint(1, 2)):
        playlist.append(commPath + commerical)

    return playlist


def movieInserter(playlist):
    choice = moviePath + random.choice(os.listdir(moviePath))
    playlist.append(choice)
    print(choice)
    return playlist