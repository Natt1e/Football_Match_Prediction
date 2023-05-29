from gevent import monkey

monkey.patch_all()
import csv
import time
from enum import Enum
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
import gevent
from gevent.queue import Queue


class finalData(object):
    def __init__(self, fightRateDif, fightGoalDif, recentRateDif, recentGoalDif, leagueRateDif, leagueGoapDif,
                 supportDif):
        self.fightRateDif = fightRateDif
        self.fightGoalDif = fightGoalDif
        self.recentRateDif = recentRateDif
        self.recentGoalDif = recentGoalDif
        self.leagueRateDif = leagueRateDif
        self.leagueGoalDif = leagueGoapDif
        self.supportDif = supportDif


class WinRateCompare(object):
    def __init__(self, teamName, homeRate, awayRate, difRate):
        self.teamName = teamName
        self.homeRate = homeRate
        self.awayRate = awayRate
        self.difRate = difRate


class twoEle(object):
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2


class matchType(Enum):
    home = 1
    neutral = 0
    away = -1


class matchData(object):
    def __init__(self, time, kind, team1, team2, score_team1, score_team2):
        self.kind = kind
        self.time = time
        self.team1 = team1
        self.team2 = team2
        self.score_team1 = score_team1
        self.score_team2 = score_team2


class leagueData(object):
    def __init__(self, name, kind, allTimes, winTimes, drawTimes, loseTimes, goalsScored, goalConceded, point, rank,
                 winningPercent):
        self.name = name
        self.kind = kind
        self.allTimes = allTimes
        self.winTimes = winTimes
        self.drawTimes = drawTimes
        self.loseTimes = loseTimes
        self.goalsScored = goalsScored
        self.goalConceded = goalConceded
        self.point = point
        self.rank = rank
        self.winningPercent = winningPercent


def changeHtmlPage(num):
    url = "https://www.dongqiudi.com/liveDetail/%s.html" % num
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,
                        '#__layout > div > div.container > div > div.live-con > div.live-left > div.tab-toggle > p:nth-child(2) > span').click()
    time.sleep(3)
    page = driver.page_source
    driver.quit()
    html1 = etree.HTML(page)
    return html1


def getSupportRate(htmlPage):
    supportRate1 = htmlPage.cssselect(
        '#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.match-vote > ul > li:nth-child(1) > div > div > div > span')[
        0].text
    supportRate2 = htmlPage.cssselect(
        '#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.match-vote > ul > li:nth-child(3) > div > div > div > span')[
        0].text
    return (float(supportRate1.strip("%")) - float(supportRate2.strip("%"))) / 100


def getMatchInfo(htmlPage, cssString):
    if not htmlPage.cssselect(cssString):
        return []
    else:
        all_recode = htmlPage.cssselect(cssString)[0]
    dataList = []
    for i in range(1, len(all_recode)):
        p = all_recode[i]
        time = 2023 - int(p[0].text.split("-")[0])
        # print(time)
        kind = p[1].text
        team1 = p[2].text
        score = p[3].text
        team2 = p[4].text
        score_team1 = score.split("-")[0]
        score_team2 = score.split("-")[1]
        # print(score_team1 + " " + score_team2)
        dataList.append(matchData(time, kind, team1, team2, score_team1, score_team2))
    return dataList


def getLeaGueRecode(page, css1, css2):
    name = page.cssselect(css1)[0].text
    if not page.cssselect(css2):
        all_info = []
    else:
        all_info = page.cssselect(css2)[0]
    dataList = []
    for i in range(1, len(all_info)):
        p = all_info[i]
        kind = p[0].text
        allTimes = p[1].text
        winTimes = p[2].text
        drawTimes = p[3].text
        loseTimes = p[4].text
        goalsScored = p[5].text
        goalConceded = p[6].text
        point = p[7].text
        rank = p[8].text
        winningPersent = p[9].text
        # print(name + " " + winningPersent)
        dataList.append(
            leagueData(name, kind, allTimes, winTimes, drawTimes, loseTimes, goalsScored, goalConceded, point, rank,
                       winningPersent))
    return dataList


def getName(page, css):
    name = page.cssselect(css)[0].text
    return name


def handleBattleRecode(dataList, homeTeam, awayTeam, type):
    if len(dataList) == 0:
        return twoEle(0, 0)
    homeDif = 0
    awayDif = 0
    winHome = 0
    drawHome = 0
    winAway = 0
    drawAway = 0
    if type == matchType.home.value:
        weight = 0.51
    else:
        weight = 0.5
    homeMatch = []
    awayMatch = []
    for data in dataList:
        if data.team1 == homeTeam and data.team2 == awayTeam:
            homeMatch.append(data)
        elif data.team1 == awayTeam and data.team2 == homeTeam:
            awayMatch.append(data)
        else:
            print("Dongqiudi is a sb, %s-%s, The match is not between %s and %s" % (
                data.team1, data.team2, homeTeam, awayTeam))

    temp1 = 0
    for data in homeMatch:
        if data.time < 15:
            timeWeight = 15 - data.time
        else:
            timeWeight = 0
        homeDif = homeDif + (float(data.score_team1) - float(data.score_team2)) * timeWeight
        if data.score_team1 > data.score_team2:
            winHome += timeWeight
        if data.score_team1 == data.score_team2:
            drawHome += timeWeight
        temp1 += timeWeight
    temp2 = 0
    for data in awayMatch:
        if data.time < 15:
            timeWeight = 15 - data.time
        else:
            timeWeight = 0
        awayDif = awayDif + (float(data.score_team2) - float(data.score_team1)) * timeWeight
        if data.score_team1 < data.score_team2:
            winAway += timeWeight
        if data.score_team1 == data.score_team2:
            drawAway += timeWeight
        temp2 += timeWeight
    if temp1 == 0:
        temp1 = 1
    if temp2 == 0:
        temp2 = 1
    timeWeight = (10 - dataList[0].time) / 10
    if timeWeight < 0:
        timeWeight = 0
    goalDif = weight * homeDif / temp1 + (1 - weight) * awayDif / temp2
    rate = weight * (winHome + 0.5 * drawHome) / temp1 + (1 - weight) * (winAway + 0.5 * drawAway) / temp2
    return twoEle(timeWeight * (rate - 0.5), timeWeight * goalDif)


def handleRecentRecode(dataList, teamName, type):
    if len(dataList) == 0:
        return twoEle(0, 0)
    homeDif = 0
    awayDif = 0
    weight = 0
    winHome = 0
    drawHome = 0
    winAway = 0
    drawAway = 0
    if type == matchType.home.value:
        weight = 0.6
    elif type == matchType.neutral.value:
        weight = 0.5
    elif type == matchType.away.value:
        weight = 0.4
    temp1 = 0
    temp2 = 0
    for data in dataList:
        if data.time < 15:
            timeWeight = 15 - data.time
        else:
            timeWeight = 0
        if data.team1 == teamName:
            homeDif = homeDif + timeWeight * (float(data.score_team1) - float(data.score_team2))
            if data.score_team1 > data.score_team2:
                winHome += timeWeight
            if data.score_team1 == data.score_team2:
                drawHome += timeWeight
            temp1 += timeWeight
        elif data.team2 == teamName:
            awayDif = awayDif + timeWeight * (float(data.score_team2) - float(data.score_team1))
            if data.score_team1 < data.score_team2:
                winAway += timeWeight
            if data.score_team1 == data.score_team2:
                drawAway += timeWeight
            temp2 += timeWeight
    if temp1 == 0:
        temp1 = 1
    if temp2 == 0:
        temp2 = 1
    timeWeight = (10 - dataList[0].time) / 10
    if timeWeight < 0:
        timeWeight = 0
    goalDif = weight * homeDif / temp1 + (1 - weight) * awayDif / temp2
    rate = weight * (winHome + 0.5 * drawHome) / temp1 + (1 - weight) * (winAway + 0.5 * drawAway) / temp2
    return twoEle(rate * timeWeight, goalDif * timeWeight)


def handleLeagueData(dataList, teamName, type):
    if len(dataList) == 0:
        return twoEle(0, 0)
    winRate = 0
    goalDif = 0
    for data in dataList:
        if data.name != teamName:
            print("Dongqiudi is a sb, The data isn't belong to %s" % teamName)
        elif data.kind == '总场' and type == matchType.neutral.value:
            winRate = (float(data.winTimes) + 0.5 * float(data.drawData)) / (float(data.allTimes))
            goalDif = (float(data.goalsScored) - float(data.goalConceded)) / (float(data.allTimes))
        elif data.kind == '总场':
            winRate += 0.5 * (float(data.winTimes) + 0.5 * float(data.drawTimes)) / ((float(data.allTimes)))
            goalDif += 0.5 * (float(data.goalsScored) - float(data.goalConceded)) / (float(data.allTimes))
        elif data.kind == '客场' and type == matchType.away.value:
            winRate += 0.5 * (float(data.winTimes) + 0.5 * float(data.drawTimes)) / (float(data.allTimes))
            goalDif += 0.5 * (float(data.goalsScored) - float(data.goalConceded)) / (float(data.allTimes))
        elif data.kind == '主场' and type == matchType.home.value:
            winRate += 0.5 * (float(data.winTimes) + 0.5 * float(data.drawTimes)) / (float(data.allTimes))
            goalDif += 0.5 * (float(data.goalsScored) - float(data.goalConceded)) / (float(data.allTimes))

    return twoEle(winRate, goalDif)


def HomeAwayWinRateDif(dataList, teamName):
    if len(dataList) == 0:
        return WinRateCompare("0", 0, 0, 0)
    homeRate = 0
    awayRate = 0
    for data in dataList:
        if data.kind == '主场':
            homeRate = float(data.winningPercent.strip("%")) / 100
        if data.kind == '客场':
            awayRate = float(data.winningPercent.strip("%")) / 100
    return WinRateCompare(teamName, homeRate, awayRate, homeRate - awayRate)


def checkPage(page):
    score = page.cssselect(
        '#__layout > div > div.container > div > div.live-con > div.live-left > div.match-info > div > div > p.score-vs')
    if not score:
        return 0
    else:
        score1 = int(score[0].text.split("-")[0])
        score2 = int(score[0].text.split("-")[1])
        if score1 >= 10 and score2 >= 10:
            return None
        elif score1 > score2:
            return 1
        elif score1 == score2:
            return 0
        else:
            return -1


def mainClass(index):
    newPage = changeHtmlPage(index)  # 手动模拟键盘操作，使网页进入目标页面
    result = checkPage(newPage)
    homeTeam = ""
    awayTeam = ""
    if result == None:
        data = None
    else:
        homeTeam = getName(newPage,
                           '#__layout > div > div.container > div > div.live-con > div.live-left > div.match-info > a:nth-child(1) > dl > dd')
        awayTeam = getName(newPage,
                           '#__layout > div > div.container > div > div.live-con > div.live-left > div.match-info > a:nth-child(3) > dl > dd')
        matchData1 = getMatchInfo(newPage,
                                  "#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.vs-history > div")  # 获取两队交手记录
        ele1 = handleBattleRecode(matchData1, homeTeam, awayTeam, matchType.home.value)
        matchData2 = getMatchInfo(newPage,
                                  '#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.recent-record > div.recent-record-teamA')  # 获取队A的近期比赛记录
        ele2 = handleRecentRecode(matchData2, homeTeam, matchType.home.value)
        matchData3 = getMatchInfo(newPage,
                                  '#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.recent-record > div.recent-record-teamB')  # 获取队B的近期比赛记录
        ele3 = handleRecentRecode(matchData3, awayTeam, matchType.away.value)
        leagueData1 = getLeaGueRecode(newPage,
                                      '#__layout > div > div.container > div > div.live-con > div.live-left > div.match-info > a:nth-child(1) > dl > dd',
                                      '#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.league-table > div > div:nth-child(1)')  # 获取队A的联赛成绩
        ele4 = handleLeagueData(leagueData1, homeTeam, matchType.home.value)
        rate1 = HomeAwayWinRateDif(leagueData1, homeTeam)  # 获取主队的主客场表现差异
        leagueData2 = getLeaGueRecode(newPage,
                                      '#__layout > div > div.container > div > div.live-con > div.live-left > div.match-info > a:nth-child(3) > dl > dd',
                                      '#__layout > div > div.container > div > div.live-con > div.live-left > div.analysis-part > div.league-table > div > div:nth-child(2)')  # 获取队B的联赛成绩
        ele5 = handleLeagueData(leagueData2, awayTeam, matchType.away.value)
        rate2 = HomeAwayWinRateDif(leagueData2, awayTeam)  # 获取客队的主客场表现差异
        supportRate = getSupportRate(newPage)
        recentRate = ele2.data1 - ele3.data1
        recentGoal = ele2.data2 - ele3.data2
        if (ele2.data1 == 0 and ele2.data2 == 0) or (ele3.data1 == 0 and ele3.data2 == 0):
            recentRate = 0
            recentGoal = 0
        leagueRate = ele4.data1 - ele5.data1
        leagueGoal = ele4.data2 - ele5.data2
        if (ele4.data1 == 0 and ele4.data2 == 0) or (ele5.data1 == 0 and ele5.data2 == 0):
            leagueRate = 0
            leagueGoal = 0
        data = finalData(ele1.data1, ele1.data2, recentRate, recentGoal, leagueRate,
                         leagueGoal, supportRate)
    if data:
        path = "predict.csv"
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [homeTeam, awayTeam, round(data.fightRateDif, 4), round(data.fightGoalDif, 4), round(data.recentRateDif, 4),
                 round(data.recentGoalDif, 4), round(data.leagueRateDif, 4),
                 round(data.leagueGoalDif, 4),
                 round(data.supportDif, 4)])
            print('分析完毕,页面索引是%s' %str(index))
    else:
        print('无效页面,页面索引是%s' % (str(index)))
