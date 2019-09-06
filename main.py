import pygame
import sys
import traceback
import myplane
from pygame.locals import *
import enemy
import bullet
import random

pygame.init()
pygame.mixer.init()

bg_size = width,height = 400,700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("外星人入侵")

background = pygame.image.load("images/background.png").convert()

WHITE = (255,255,255)

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.mp3")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
big_enemy_flying_sound = pygame.mixer.Sound("sound/big_spaceship_flying.wav")
big_enemy_flying_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/game_over.wav")
me_down_sound.set_volume(0.2)
button_down_sound = pygame.mixer.Sound("sound/button.wav")
button_down_sound.set_volume(0.2)
level_up_sound = pygame.mixer.Sound("sound/achievement.wav")
level_up_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)

def add_small_enemies(group1,group2,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1,group2,num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me  = myplane.MyPlane(bg_size)

    enemies =pygame.sprite.Group()

    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)

    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 5)

    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET_NUM = 4
    for i in range(BULLET_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))


    clock = pygame.time.Clock()

    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    score = 0
    score_font = pygame.font.Font("font/font.ttf",36)

    #标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("images/game_pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/game_pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/game_resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/game_resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left,paused_rect.top = width - paused_rect.width-10,10
    paused_image = pause_nor_image

    #设置难度级别
    level = 1

    #全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf",48)
    bomb_num = 3


    #生命數量
    life_image = pygame.image.load("images/plane.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #阻止反復打開記錄文件
    recorded = False

    #游戲結束
    gameover_image = pygame.image.load("images/gameover.png")
    gameover_rect = gameover_image.get_rect()

    #用于切换图片
    switch_image = True

    #用于延迟
    delay = 100

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom >0:
                                each.active = False



        #根据用户得分增加难度
        if level == 1 and score>50000:
            level = 2
            #增加3小，2中，1大
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            #提升小型敌机速度
            inc_speed(small_enemies,1)
        elif level == 2 and score>300000:
            level = 3
            # 增加5小，3中，2大
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies,1)
        elif level == 3 and score>600000:
            level = 4
            # 增加5小，3中，2大
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies,1)
        elif level == 4 and score>1000000:
            level = 5
            # 增加5小，3中，2大
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)




        screen.blit(background, (0, 0))

        if life_num and not paused:
            #检测用户键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_RIGHT]:
                me.moveRight()


            #发射子弹
            if not(delay%10):
                bullet_sound.play()
                bullet1[bullet1_index].reset(me.rect.midtop)
                bullet1_index = (bullet1_index+1)%BULLET_NUM

            for b in bullet1:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                               e.active = False

            #绘制大型飞机
            for each in big_enemies:
              if each.active:
                  each.move()
                  screen.blit(each.image,each.rect)
                  #播放出现音效
                  if each.rect.bottom>-50:
                     big_enemy_flying_sound.play()
              else:
                  if not (delay%3):
                      screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                      e3_destroy_index = (e3_destroy_index+1)%6
                      if e3_destroy_index == 0:
                        enemy3_down_sound.play()
                        score += 10000
                        each.reset()

            #绘制中型敌机
            for each in mid_enemies:
                if each.active:
                   each.move()
                   screen.blit(each.image,each.rect)
                else:
                    if not (delay % 3):
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        score += 6000
                        each.reset()

            #绘制小型敌机
            for each in small_enemies:
                 if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                 else:
                     if e1_destroy_index == 0:
                         enemy1_down_sound.play()
                     if not (delay % 3):
                         screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                         e1_destroy_index = (e1_destroy_index + 1) % 4
                         if e1_destroy_index == 0:
                             score += 1000
                             each.reset()

            enemies_down = pygame.sprite.spritecollide(me,enemies,False)
            if enemies_down:
                me.active = False
                for e in enemies_down:
                    e.active = False


            #绘制我方飞机
            if me.active:
                 if switch_image:
                      screen.blit(me.image1,me.rect)
                 else:
                      screen.blit(me.image2,me.rect)
            else:
                me_down_sound.play()
                if not (delay%3):
                    screen.blit(me.destroy_images[me_destroy_index],me.rect)
                    me_destroy_index = (me_destroy_index+1)%3
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()

        elif life_num == 0:
            #游戲結束
            screen.blit(gameover_image, gameover_rect)
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            if not recorded:
                recorded = True
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:  # 如果玩家得分大于历史最高分，则将当前分数存档
                    with open("record.txt", "w") as f:
                        f.write(str(score))
                        record_score_text = score_font.render("%d" % record_score, True, WHITE)
                        screen.blit(record_score_text, (150, 25))
                        game_over_score_text = score_font.render("%d" % score, True, WHITE)
                        screen.blit(game_over_score_text, (180, 370))



        #绘制全屏炸弹数量
        bomb_text = bomb_font.render("X %d"% bomb_num,True,WHITE)
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image,(10,height-10-bomb_rect.height))
        screen.blit(bomb_text,(20+bomb_rect.width,height-5-text_rect.height))

        #繪製生命數量
        if life_num:
            for i in range(life_num):
                screen.blit(life_image,\
                            (width-10-(i+1)*life_rect.width,\
                             height-10-life_rect.height))
        #绘制得分
        score_text = score_font.render("Score : %s"%str(score),True,WHITE)
        screen.blit(score_text,(10,5))



        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)


        #切换图片
        if not (delay%5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()