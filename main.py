import threading

from discord.ext import commands
import time
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

'''while True:
    ytp-ad-text ytp-ad-skip-button-text'''

TOKEN = ''
client = commands.Bot(command_prefix=';')


@client.event
async def on_ready():
    print(client.user.id)
    print("ready")


sched = BackgroundScheduler()


@sched.scheduled_job('cron', hour='08', minute='00', id='test_1')
def background_task():
    file = open("Data.txt", "r+")  # txt 파일 불러오기
    strings = file.readlines()
    file.close()

    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver = webdriver.Chrome(r'C:\chromedriver.exe', chrome_options=options)

    for string in strings:
        if len(string) < 5:
            continue
        print('실행중')
        user_id = string.split(":")[0]
        pw = string.split("&4")[1]

        if pw == '*':
            continue

        name_temp = string.split(user_id + ":")[1]
        city_temp = name_temp.split("&1")[1]
        school_temp = city_temp.split("&2")[1]
        birth_temp = school_temp.split("&3")[1]

        name = name_temp.split("&1")[0]
        city = city_temp.split("&2")[0]
        school = school_temp.split("&3")[0]
        birth = birth_temp.split("&4")[0]

        select_city = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원',
                       '충청북', '충청남', '전라북', '전라남', '경상북', '경상남', '제주']
        select_city2 = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원',
                        '충북', '충남', '전북', '전남', '경북', '경남', '제주']
        cnt = 0
        opts1 = 0
        for c in select_city:
            if c in city:
                cnt += 1
                opts1 = select_city.index(c) + 2

        if not cnt:
            for c in select_city2:
                if c in city:
                    cnt += 1
                    opts1 = select_city2.index(c) + 2

        if not cnt or cnt > 1:
            continue

        name = str(name)
        school = str(school)
        birth = str(birth)
        pw = str(pw)
        opts2 = '5'  # '고등학교' 옵션

        url = "https://hcs.eduro.go.kr/#/loginHome"
        driver.get(url)
        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 5)
        short_wait = WebDriverWait(driver, 1)

        # Go 버튼
        button = driver.find_element_by_id('btnConfirm2')
        button.click()

        # 학교 검색 버튼
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchBtn'))).click()

        time.sleep(1)
        # 지역 선택
        try:
            button = driver.find_element_by_xpath("//*[@id=\"sidolabel\"]/option[" + str(opts1) + "]")
            button.click()
        except:
            #driver.quit()
            continue

        # 현재 직업 선택
        button = driver.find_element_by_xpath("//*[@id=\"crseScCode\"]/option[" + str(opts2) + "]")
        button.click()

        # 학교명 입력
        wait.until(EC.element_to_be_clickable((By.ID, 'orgname'))).click()
        user_input = driver.find_element_by_id('orgname')
        user_input.send_keys(school)

        time.sleep(1)
        # 학교 검색 버튼
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchBtn'))).click()
        except:
            #driver.quit()
            continue

        time.sleep(1)

        # 검색된 학교 선택
        try:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/ul/li/a"))).click()
        except:
            #driver.quit()
            continue

        time.sleep(1)
        # 확인 버튼
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'layerFullBtn'))).click()

        # 성명 입력
        wait.until(EC.element_to_be_clickable((By.ID, 'user_name_input'))).click()
        user_input = driver.find_element_by_id('user_name_input')
        user_input.send_keys(name)

        # 생년월일 입력
        wait.until(EC.element_to_be_clickable((By.ID, 'birthday_input'))).click()
        user_input = driver.find_element_by_id('birthday_input')
        user_input.send_keys(birth)

        # 확인 버튼
        try:
            short_wait.until(EC.element_to_be_clickable((By.ID, 'btnConfirm'))).click()
        except:
            #driver.quit()
            continue

        time.sleep(1)
        # 비밀번호 입력
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'input_text_common'))).click()

        pyperclip.copy(pw)  # 비밀번호 클립보드에 복사
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  # 붙여넣기
        pyperclip.copy('reset')  # 클립보드에서 비밀번호 삭제

        # 비밀번호 확인 버튼
        wait.until(EC.element_to_be_clickable((By.ID, 'btnConfirm'))).click()

        # 목록에서 이름과 일치하는 사람 선택
        '''wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'name')))'''
        '''searched_names1 = driver.find_elements_by_class_name("name")'''

        time.sleep(1)
        cnt = 1
        try:
            driver.find_element_by_xpath(
                "//*[@id=\"container\"]/div/section[2]/div[2]/ul/li/a/span[1]").click()
        except:
            while True:
                try:
                    print("1")
                    searched_name2 = driver.find_element_by_xpath(
                        "//*[@id=\"container\"]/div/section[2]/div[2]/ul/li[" + str(cnt) + "]/a/span[1]")
                    s_name = searched_name2.text.split("(")[0]
                    s_name = s_name.strip()
                    if s_name == name:
                        searched_name2.click()
                        break
                except:
                    #driver.quit()
                    continue
                cnt += 1

        # 1번 문항 아니요
        try:
            wait.until(EC.element_to_be_clickable((By.ID, 'survey_q1a1'))).click()
        # "예" 대답은 클래스명이 a2로 끝남
        # wait.until(EC.element_to_be_clickable((By.ID, 'survey_q1a2'))).click()
        except:
            continue

        # 2번 문항 아니요
        short_wait.until(EC.element_to_be_clickable((By.ID, 'survey_q2a1'))).click()

        # 3번 문항 아니요
        short_wait.until(EC.element_to_be_clickable((By.ID, 'survey_q3a1'))).click()

        # 제출 버튼
        short_wait.until(EC.element_to_be_clickable((By.ID, 'btnConfirm'))).click()
        print('실행 완료')

    driver.quit()  # 웹 드라이버 끄기
    print('실행 전부 완료')


sched.start()


@client.command(aliases=['자동'])
async def auto(ctx, pw='test'):
    user_id = str(ctx.author.id)
    file = open("Data.txt", "r+")  # txt 파일 불러오기
    strings = file.readlines()
    file.close()

    # 사용자 정보 위치 찾기
    locate = -1
    for word in strings:
        if user_id in word:
            locate = strings.index(word)

    file = open("Data.txt", "r+")
    strings = file.readlines()
    file.close()
    string = strings[locate]

    if locate != -1:

        if string.split("&4")[1] == "*" and pw.isdigit():
            front = string.split("&4")[0]
            changed_string = front + "&4" + pw
            saved = "\n".join(strings)
            write = saved.replace(string, changed_string)
            with open("Data.txt", "w+") as file:
                file.write(write)
            await ctx.send('자동 모드 활성화')

        elif not string.split("&4")[1] == "*" and pw.isdigit():
            front = string.split("&4")[0]
            changed_string = front + "&4" + pw
            saved = "\n".join(strings)
            write = saved.replace(string, changed_string)
            with open("Data.txt", "w+") as file:
                file.write(write)
            await ctx.send('비밀번호가 변경완료')

        elif pw == 'test':
            front = string.split("&4")[0]
            changed_string = front + "&4" + pw
            saved = "\n".join(strings)
            write = saved.replace(string, changed_string)
            with open("Data.txt", "w+") as file:
                file.write(write)
            await ctx.send('자동 모드 비활성화')

    if locate == -1:
        await ctx.send('데이터가 없습니다')


@client.command(aliases=['nothing'])
async def p(ctx, name=None, city=None, school=None, birth=None, pw=None, check=None):
    helping_msg1 = '명령어는 ";p <본인 이름> <지역> <학교 이름> <생년월일 6자리> <비밀번호 4자리>" 입니다'
    helping_msg2 = "지역은 '서울', '부산', '대구', '인천', '광주', '대전'," \
                   " '울산', '세종', '경기', '강원', '충청북', '충청남', '전라북', '전라남'," \
                   " '경상북', '경상남', '제주' 중 하나를 적어주세요"

    select_city = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원',
                   '충청북', '충청남', '전라북', '전라남', '경상북', '경상남', '제주']
    select_city2 = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기', '강원',
                    '충북', '충남', '전북', '전남', '경북', '경남', '제주']

    if not name:
        return await ctx.send(helping_msg1)

    user_id = str(ctx.author.id)  # ID 따오기
    file = open("Data.txt", "r+")  # txt 파일 불러오기
    strings = file.readlines()
    file.close()

    # 사용자 정보 위치 찾기
    locate = -1
    for word in strings:
        if user_id in word:
            locate = strings.index(word)

    if locate != -1 and name.isdigit() and city is None:
        # 사용자 정복 존재할 때 정보 불러오기
        file = open("Data.txt", "r+")
        strings = file.readlines()
        file.close()
        name_temp = strings[locate].split(user_id + ":")[1]
        city_temp = name_temp.split("&1")[1]
        school_temp = city_temp.split("&2")[1]
        birth_temp = school_temp.split("&3")[1]

        pw = name
        name = name_temp.split("&1")[0]
        city = city_temp.split("&2")[0]
        school = school_temp.split("&3")[0]
        birth = birth_temp.split("&4")[0]

    if locate == -1 and str(name).isdigit and city is None:
        await ctx.send('데이터가 없습니다')

    cnt = 0
    opts1 = 0
    for c in select_city:
        if c in city:
            cnt += 1
            opts1 = select_city.index(c) + 2

    if not cnt:
        for c in select_city2:
            if c in city:
                cnt += 1
                opts1 = select_city2.index(c) + 2

    if check:
        return await ctx.send(helping_msg1)

    if not cnt and pw is None:
        return await ctx.send(helping_msg1)

    if not cnt or cnt > 1:
        return await ctx.send(helping_msg2)

    if not birth.isdigit() or not len(str(birth)) == 6:
        return await ctx.send(helping_msg1)

    if not pw.isdigit() or not len(str(pw)) == 4:
        return await ctx.send(helping_msg1)

    # 사용자 정보가 존재하지 않는데 숫자만 입력할 때
    if locate == -1 and name.isdigit():
        return await ctx.send("저장된 데이터가 없습니다")

    name = str(name)
    city = str(city)
    school = str(school)
    birth = str(birth)
    pw = str(pw)
    opts2 = '5'  # '고등학교' 옵션

    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # driver = webdriver.Chrome(r'C:\chromedriver.exe')
    driver = webdriver.Chrome(r'C:\chromedriver.exe', chrome_options=options)

    url = "https://hcs.eduro.go.kr/#/loginHome"
    driver.get(url)
    driver.implicitly_wait(10)

    wait = WebDriverWait(driver, 5)
    short_wait = WebDriverWait(driver, 1)

    # Go 버튼
    button = driver.find_element_by_id('btnConfirm2')
    button.click()

    # 학교 검색 버튼
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchBtn'))).click()

    time.sleep(1)
    # 지역 선택
    try:
        button = driver.find_element_by_xpath("//*[@id=\"sidolabel\"]/option[" + str(opts1) + "]")
        button.click()
    except:
        driver.quit()
        return await ctx.send("지역 에러")

    # 현재 직업 선택
    button = driver.find_element_by_xpath("//*[@id=\"crseScCode\"]/option[" + str(opts2) + "]")
    button.click()

    # 학교명 입력
    wait.until(EC.element_to_be_clickable((By.ID, 'orgname'))).click()
    user_input = driver.find_element_by_id('orgname')
    user_input.send_keys(school)

    time.sleep(1)
    # 학교 검색 버튼
    try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'searchBtn'))).click()
    except:
        driver.quit()
        return await ctx.send("검색된 학교가 없습니다")

    time.sleep(1)

    # 검색된 학교 선택
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/ul/li/a"))).click()
    except:
        driver.quit()
        return await ctx.send("검색 결과가 너무 많거나 없습니다")

    time.sleep(1)
    # 확인 버튼
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'layerFullBtn'))).click()

    # 성명 입력
    wait.until(EC.element_to_be_clickable((By.ID, 'user_name_input'))).click()
    user_input = driver.find_element_by_id('user_name_input')
    user_input.send_keys(name)

    # 생년월일 입력
    wait.until(EC.element_to_be_clickable((By.ID, 'birthday_input'))).click()
    user_input = driver.find_element_by_id('birthday_input')
    user_input.send_keys(birth)

    # 확인 버튼
    try:
        short_wait.until(EC.element_to_be_clickable((By.ID, 'btnConfirm'))).click()
    except:
        driver.quit()
        return await ctx.send("이름 또는 생년월일을 다시 확인해주세요")

    time.sleep(1)
    # 비밀번호 입력
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'input_text_common'))).click()

    pyperclip.copy(pw)  # 비밀번호 클립보드에 복사
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()  # 붙여넣기
    pyperclip.copy('reset')  # 클립보드에서 비밀번호 삭제

    # 비밀번호 확인 버튼
    wait.until(EC.element_to_be_clickable((By.ID, 'btnConfirm'))).click()

    # 목록에서 이름과 일치하는 사람 선택
    '''wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'name')))'''
    '''searched_names1 = driver.find_elements_by_class_name("name")'''

    time.sleep(1)
    cnt = 1
    try:
        driver.find_element_by_xpath(
            "//*[@id=\"container\"]/div/section[2]/div[2]/ul/li/a/span[1]").click()
    except:
        while True:
            try:
                print("1")
                searched_name2 = driver.find_element_by_xpath(
                    "//*[@id=\"container\"]/div/section[2]/div[2]/ul/li[" + str(cnt) + "]/a/span[1]")
                s_name = searched_name2.text.split("(")[0]
                s_name = s_name.strip()
                if s_name == name:
                    searched_name2.click()
                    break
            except:
                driver.quit()
                return await ctx.send('일치하는 이름의 항목이 없습니다')
            cnt += 1

    # 1번 문항 아니요
    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'survey_q1a1'))).click()
    # "예" 대답은 클래스명이 a2로 끝남
    # wait.until(EC.element_to_be_clickable((By.ID, 'survey_q1a2'))).click()
    except:
        await ctx.send("자가진단 제출은 3분에 한번 가능합니다")

    # 2번 문항 아니요
    short_wait.until(EC.element_to_be_clickable((By.ID, 'survey_q2a1'))).click()

    # 3번 문항 아니요
    short_wait.until(EC.element_to_be_clickable((By.ID, 'survey_q3a1'))).click()

    # 제출 버튼
    short_wait.until(EC.element_to_be_clickable((By.ID, 'btnConfirm'))).click()

    driver.quit()  # 웹 드라이버 끄기

    locate = -1
    for word in strings:
        if user_id in word:
            locate = strings.index(word)

    # 사용자 정보가 존재하지 않을때 사용자 정보를 파일에 저장
    if locate == -1:
        file = open("Data.txt", "r+")
        last = file.readlines()
        file.close()
        last = "\n".join(last)

        with open("Data.txt", "w+") as file:
            file.write(last + '\n' + user_id + ":" + name + '&1' + city + '&2' + school + '&3' + birth + '&4' + "*")

    await ctx.send("작업이 완료되었습니다!")


client.run(TOKEN)
