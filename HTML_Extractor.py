#pls no bully I only know how to code in dumb inelegant ways
import urllib.request,csv
urllocation=str(input('Input path to the saved results:')) #asks for the path to the saved html
page = urllib.request.urlopen(urllocation).read().decode('utf-8') #reads the html and decodes it into a slightly friendlier format
startidx=0 #initialize starting index
teamlist1=[] #initialize empty list for teamlist 1
teamscore1=[] #blah
teamlist2=[] #blah2
teamscore2=[] #blah3
statuslist=[] #blah4
datelist=[] #it's empty just like my life ha-ha get it??
#print(page)
while page.find('GameID=',startidx)!=-1:
    #the html code precedes any game result with the game ID first. it will end the team name with a nbsp:
    #non-breaking space apparently and end the score with the same thing. for team 2 it won't add that to the score.
    gameidx=page.find('GameID=',startidx)
    teamnameidx1=page.find('>',gameidx)+8 #shift by 4 bytes because of line breaks
    teamnameidx2=page.find('&nbsp',teamnameidx1)
    teamlist1.append(page[teamnameidx1:teamnameidx2])
    teamscoreidx1=page.find('>',teamnameidx2)+1
    teamscoreidx2 =min(page.find('&nbsp', teamscoreidx1),page.find('<', teamscoreidx1))
    teamscore1.append(page[teamscoreidx1:teamscoreidx2])

    #get the status of the game and the date before we reset the gameidx(because I'm lazy)
    statusidx=page.rfind('verdana">',startidx,gameidx) #this gives the index right before the game id
    statusidx=page.rfind('verdana">',startidx, statusidx) #repeat for the one right before the status
    statusendidx=page.find('\r\n',statusidx+10)
    statuslist.append(page[statusidx+16:statusendidx])

    dateidx=page.rfind('verdana">',startidx, statusidx)+9 #get index before status
    dateendidx=page.find('</font',dateidx) #get end index for the date
    datelist.append(page[dateidx:dateendidx])

    gameidx=max(page.find('>',teamscoreidx2),page.find(';',teamscoreidx2))
    teamnameidx1=gameidx+13 #more index shifts to get the team names nicely, don't worry about it
    teamnameidx2=page.find('&nbsp',teamnameidx1)
    teamlist2.append(page[teamnameidx1:teamnameidx2])
    teamscoreidx1=page.find('>',teamnameidx2)+1
    teamscoreidx2 = page.find('</font', teamscoreidx1)
    teamscore2.append(page[teamscoreidx1:teamscoreidx2])
    startidx=teamscoreidx2

#for debugging
#print(teamlist1)
#print(teamscore1)
#print(teamlist2)
#print(teamscore2)
#print(datelist)
#print(statuslist)

teamlist=set(teamlist1)
for team in teamlist:
    a = open(f'{team}.csv', 'w', newline='')
    writer = csv.writer(a)
    gameidx = 0
    while gameidx<len(teamscore1):
        if teamlist1[gameidx]==team or teamlist2[gameidx]==team:
            result='Win' #default to win, change to loss if lose conditions ar emet
            if (statuslist[gameidx]=='FFV' or teamscore2[gameidx]<teamscore1[gameidx]) and teamlist2[gameidx]==team:
                result='Loss'
            elif (statuslist[gameidx]=='FFH' or teamscore1[gameidx]<teamscore2[gameidx]) and teamlist1[gameidx]==team:
                result='Loss'
            newrow=[teamlist1[gameidx],teamscore1[gameidx],teamlist2[gameidx],teamscore2[gameidx],datelist[gameidx],statuslist[gameidx],result]
            writer.writerow(newrow)
        gameidx+=1
    a.close()