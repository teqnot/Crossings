import pygame, os, time, json, re
from pygame.transform import scale

width1 = 600
height1 = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 148, 255)
TOAD_IN_LOVE = (60, 170, 60)
values = []
ho = False
xx = 0


def main():
    global screen, fon, fon_rect, button_go, button_rect, all_sprites, image_path, task_path, resource_path, data, boat, characters_surf, flag, flag3, in_boat, distance, left_v, right_v, values_r, flag2, flag4, winflag, click_character, flag5, click_sound, gameover_sound, win_sound
    current_path = os.path.dirname(__file__)  # Where your .py file is located
    resource_path = os.path.join(current_path, 'src_img')  # The resource folder path
    image_path = os.path.join(resource_path, 'characters')
    task_path = os.path.join(current_path, 'tasks')

    pygame.init()

    flag = 0
    flag3 = 0
    flag2 = 0
    distance = 0
    flag4 = 0
    flag5 = 0
    winflag = 0
    click_sound = pygame.mixer.Sound('click.wav')
    gameover_sound = pygame.mixer.Sound('game_over.wav')
    win_sound = pygame.mixer.Sound('game_win.wav')
    characters_surf = []# ready characters surfaces
    in_boat = []
    left_v = []
    right_v = []
    values_r = []
    click_character = False

    screen = pygame.display.set_mode((width1, height1))
    fon = pygame.image.load("src_img/fon2.png")
    fon_rect = fon.get_rect()
    button_go = scale(pygame.image.load("src_img/button_go.png"), (50, 50))
    boat = Boat()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(boat)
    button_rect = button_go.get_rect()
    button_rect.centerx = 300
    button_rect.centery = 500
    main_menu()


def get_key(dataq):
    for value in dataq:
        if dataq[value]['rect'][0] == boat.rect.x and dataq[value]['rect'][1] == boat.rect.y - 20:
            k = value
            return k


def runGame(run, task_name):
    global screen, fon, fon_rect, button_go, button_rect, all_sprites, image_path, task_path, data, boat, characters_surf, flag, ho, flag3, distance, wows, left_v, right_v, values_r, flag2, flag4, winflag, click_character, flag5, click_sound

    with open(f'tasks\{task_name}', 'r') as f:
        data = json.load(f)
    print(data)

    for j in data:
        characters_surf.append(scale(pygame.image.load(os.path.join(image_path, str(j))), (60, 60)))

    while run:
        if len(left_v) == 3:
            win()

        x = list(pygame.mouse.get_pos())[0]
        y = list(pygame.mouse.get_pos())[1]
        click = pygame.mouse.get_pressed()

        screen.fill(WHITE)
        screen.blit(fon, fon_rect)
        screen.blit(button_go, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(x, y) and event.button == 1:
                    click_sound.play()
                    boat.moving = True
                    boat.hit = False
                    click_character = False
                    boat.update()
                    flag5 += 1
                    print(flag5)

                    if len(left_v) == 2 and boat.pos == 'right':
                        print('left vv', left_v)
                        if int(data1[left_v[0]]['ir']) - int(data1[left_v[-1]]['ir']) == 1 or int(
                                data1[left_v[-1]]['ir']) - int(data1[left_v[0]]['ir']) == 1:
                            run = False
                            game_over()

                    if len(right_v) == 2 and boat.pos == 'left':
                        if int(data1[right_v[0]]['ir']) - int(data1[right_v[-1]]['ir']) == 1 or int(
                                data1[right_v[-1]]['ir']) - int(data1[right_v[0]]['ir']) == 1:
                            run = False
                            game_over()

        if flag3 == 1:
            for k4 in data1:
                char33 = scale(pygame.image.load(os.path.join(image_path, str(k4))), (60, 60))
                screen.blit(char33, (data1[k4]['rect'][0], data1[k4]['rect'][1]))
        else:
            for key1 in data:
                char = scale(pygame.image.load(os.path.join(image_path, str(key1))), (60, 60))
                screen.blit(char, (data[key1]['rect'][0], data[key1]['rect'][1]))
                while flag <= 1:
                    data1 = data.copy()
                    flag += 1

        if boat.hit == True and boat.moving == False:
            for k in data1:
                if x in range(data1[k]['rect'][0], data1[k]['rect'][0] + 60) and y in range(data1[k]['rect'][1], data1[k]['rect'][1] + 60) and click[0]:
                    if (boat.pos == 'left' and data1[k]['location'] == 'left') or (boat.pos == 'right' or boat.pos == 'a' and data1[k]['location'] == 'right'):
                        click_sound.play()
                        print(x, y, '- [in] -', data1[k]['rect'][0] + 60, data1[k]['rect'][1] + 60)
                        data1[k]['rect'] = [boat.rect.x, boat.rect.y - 20]
                        key = get_key(data1)
                        if key == 'char3.png':
                            ho = True
                        print('chosen character', key)
                        in_boat.append(key)
                        data1[key]['location'] = 'boat'
                        click_character = True

                        if key in right_v:
                            right_v.remove(key)

                        elif key in left_v:
                            left_v.remove(key)

        for k1 in data1:
            if distance == k1:
                distance += 150

            else:
                if boat.hit == True and (data1[k1]['location'] == 'boat' and data1[k1]['boat'] != 'yes') and boat.pos == 'left' and click_character == False:
                    if k1 in in_boat:
                        in_boat.remove(k1)

                    if distance >= 600:
                        distance = 0

                    data1[k1]['location'] = 'left'
                    data1[k1]['rect'] = [20, distance]

                    if k1 not in left_v:
                        left_v.append(k1)
                        print('LEFT', left_v)

                    flag3 = 1
                    distance += 150

            if wows >= 2:
                for k2 in data1:
                    if boat.hit == True and (data1[k2]['location'] == 'boat' and data1[k2]['boat'] != 'yes') and boat.pos == 'right' and click_character == False:
                        if k2 in in_boat:
                            in_boat.remove(k2)

                        data1[k2]['location'] = 'right'
                        data1[k2]['rect'] = [470, distance]

                        if k2 not in right_v:
                            right_v.append(k2)
                            print('RIGHT', right_v)

                        print('right_v', right_v)
                        flag3 = 1

        try:
            if len(in_boat) == 2:
                key3 = scale(pygame.image.load(os.path.join(image_path, str(in_boat[0]))), (60, 60))
                character1 = scale(pygame.image.load(os.path.join(image_path, str(in_boat[-1]))), (60, 60))
                screen.blit(key3, (boat.rect.x + 40, boat.rect.y - 20))
                screen.blit(character1, (boat.rect.x, boat.rect.y - 20))
                data.pop(key)

                if key == 'char3.png':
                    data1.pop(key)

            elif len(in_boat) == 1:
                for samsa in in_boat:
                    key2 = scale(pygame.image.load(os.path.join(image_path, str(samsa))), (60, 60))
                screen.blit(key2, (boat.rect.x, boat.rect.y - 20))
                data.pop(key)
                if key == 'char3.png':
                    data1.pop(key)
        except:
            pass

        all_sprites.draw(screen)
        pygame.display.update()
        flag5 = 0

def game_over():
    global click_sound, gameover_sound
    f1 = pygame.font.Font('freesansbold.ttf', 50)
    gameOver_text = f1.render('Игра Окончена!', 1, (BLACK))
    button_back = pygame.image.load("src_img/button_back_to_menu.png")
    button_back_rect = button_back.get_rect()
    button_back_rect.centerx = 300
    button_back_rect.centery = 400

    gameover_sound.play()

    while True:
        x_back = list(pygame.mouse.get_pos())[0]
        y_back = list(pygame.mouse.get_pos())[1]
        click0 = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                False
            elif event.type == pygame.KEYDOWN:
                pass

        screen.blit(gameOver_text, (100, 200))
        screen.blit(button_back, button_back_rect)

        if button_back_rect.collidepoint(x_back, y_back) and click0[0]:
            click_sound.play()
            main()

        pygame.display.update()

def win():
    global click_sound, win_sound
    f2 = pygame.font.Font('freesansbold.ttf', 50)
    win_text = f2.render('Победа!', 1, (BLACK))
    button_win = pygame.image.load("src_img/button_back_to_menu.png")
    button_win_rect = button_win.get_rect()
    button_win_rect.centerx = 300
    button_win_rect.centery = 400

    win_sound.play()

    while True:
        x_win = list(pygame.mouse.get_pos())[0]
        y_win = list(pygame.mouse.get_pos())[1]
        click3 = pygame.mouse.get_pressed()

        for event3 in pygame.event.get():
            if event3.type == pygame.QUIT:
                False
            elif event3.type == pygame.KEYDOWN:
                pass

        screen.blit(win_text, (200, 200))
        screen.blit(button_win, button_win_rect)

        if button_win_rect.collidepoint(x_win, y_win) and click3[0]:
            click_sound.play()
            main()

        pygame.display.update()


def main_menu():
    global click_sound
    print('main menu active')

    tasks = os.listdir(task_path)
    print(tasks)
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('ВКЗ', True, BLACK)
    taskFont = pygame.font.Font('freesansbold.ttf', 36)

    button_x = 200
    button_y = 350

    count = 1
    button_dict = {}
    run1 = True
    flag1 = 1

    while run1:
        x_task = list(pygame.mouse.get_pos())[0]
        y_task = list(pygame.mouse.get_pos())[1]
        click1 = pygame.mouse.get_pressed()

        while count <= len(tasks):
            button_task = pygame.image.load('src_img/button_task.png')
            count += 1

        while flag1 <= len(tasks):
            for sch in tasks:
                button_dict[sch] = {'rect': (button_x, button_y), 'button': button_task}
                task = taskFont.render(f'Задача {flag1}', 1, BLACK)
                button_y += 50
                print(button_dict)
                flag1 += 1

        screen.fill(TOAD_IN_LOVE)
        screen.blit(titleSurf1, (200, 100))

        for schet2 in button_dict:
            screen.blit(button_dict[schet2]['button'], button_dict[schet2]['rect'])
            screen.blit(task, (button_x + 15, button_y - 30))

        for wow in button_dict:
            if x_task in range(button_dict[wow]['rect'][0], button_dict[wow]['rect'][0] + 200) and y_task in range(button_dict[wow]['rect'][1], button_dict[wow]['rect'][1] + 70) and click1[0]:
                click_sound.play()
                print(x_task, y_task, '[in]', button_dict[wow]['rect'][0], button_dict[wow]['rect'][1])
                runGame(True, wow)

        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                run1 = False
            elif event1.type == pygame.KEYDOWN:
                pass

        pygame.display.update()

class Boat(pygame.sprite.Sprite):
    def __init__(self):
        global wows
        pygame.sprite.Sprite.__init__(self)
        self.image = scale(pygame.image.load('src_img/boat.png'), (100, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = 410
        self.rect.bottom = 300
        self.xvel = 0
        self.pos = 'a'
        self.coords = []
        self.moving = False
        self.hit = True
        wows = 0

    def update(self):
        global wows
        global xx
        global ho

        if not (ho):
            pass

        else:
            while self.hit == False:
                if self.rect.x == 140:
                    self.hit = True
                    self.moving = False

                if self.rect.x == 350:
                    self.hit = True
                    self.moving = False

                if self.pos == 'right' or self.pos == 'a':
                    self.xvel = -1
                    self.rect.x += self.xvel
                    xx = self.rect.x

                if self.pos == 'left':
                    self.xvel = 1
                    self.rect.x += self.xvel
                    xx = self.rect.x

            if self.rect.x <= 150:
                self.pos = 'left'
                self.xvel = 0
                print(self.pos)

            if self.rect.x >= 350:
                self.pos = 'right'
                self.xvel = 0
                print(self.pos)
                wows += 1
                print('wows', wows)


if __name__ == '__main__':
    main()