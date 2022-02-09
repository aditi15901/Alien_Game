from blessed import Terminal
import random
import copy
from collections import deque

term =Terminal()
UP = term.KEY_UP
DOWN = term.KEY_DOWN
LEFT = term.KEY_LEFT
RIGHT = term.KEY_RIGHT
direction =RIGHT

BORDER ='💟'
BODY = '🌑' 
FOOD = ('💗','💝','💖','💕','🤍','💜','💙','💚','🧡','💛')
SPACE ='  '
FACE= ('🗿','🙉','🙂','😀','🙈','🤌','😄','😁','😊','🥺','🥰','🌚','🥵','🥳','😏','🤩','🦄','😎','🌸','💯','🐻','🐼','🌷','🌝','✨','🔥','😱','🤯','😳','👑')
HEAD='👽'
HUE='💢'

snake = deque([[5,4],[5,3],[5,2]]) #initial snake position
last_head=[5,4]
h,w=10, 15
food = [5,10] #initial position of food
score = 0
speed = 3 #initial speed
max_speed = 6
hoe=False
last_food=''
food_counter=0
hue_counter=0
hue_list=deque([])
erase=deque([])
obstacle=0

def empty_spaces_list(board, space):
  list = []
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == space:
        list.append([i, j])
  return list

with term.cbreak(), term.hidden_cursor():
    
    print(term.home + term.clear)

    board = [[SPACE] * w for _ in range(h)]
    for i in range(h):
        board[i][0] = BORDER
        board[i][-1] = BORDER
    for j in range(w):
        board[0][j] = BORDER
        board[-1][j] = BORDER

    for s in snake:
        board[s[0]][s[1]] = BODY
        if s==snake[0]:
            board[s[0]][s[1]] = HEAD

    board[food[0]][food[1]] = FOOD[0]
    last_food=FOOD[0]

    for row in board:
        print(''.join(row))
    print('Use the arrow keys!')
    print('Press Q to Quit')

    val = ''
    moving = False

    while val.lower()!='q':
        val = term.inkey(timeout = 1/speed)
        if val.code in [UP, RIGHT, DOWN]:
            moving = True
        if not moving:
            continue

        if val.code==UP and direction!=DOWN:
            direction= UP
        elif val.code==LEFT and direction!=RIGHT:
            direction=LEFT
        elif val.code==RIGHT and direction!=LEFT:
            direction=RIGHT
        elif val.code==DOWN and direction!=UP:
            direction=DOWN
        
        head = copy.copy(snake[0])

        if direction== UP:
            head[0]-=1
        elif direction== DOWN:
            head[0]+=1
        if direction== LEFT:
            head[1]-=1
        if direction== RIGHT:
            head[1]+=1

        heading= board[head[0]][head[1]]
        win=False
        if heading == last_food:
            win=True
            empty_spaces= empty_spaces_list(board, SPACE)
            food=random.choice(empty_spaces)
            if food_counter==len(FOOD)-1:
                food_counter=-1
            board[food[0]][food[1]]=FOOD[(food_counter+1)]
            last_food=FOOD[food_counter+1]
            food_counter+=1
            empty_spaces= empty_spaces_list(board, SPACE)
            hue=random.choice(empty_spaces)
            board[hue[0]][hue[1]]=HUE
            obstacle=0
            # erase=deque([])
            obstacle=1 if food[0]+1<9 and board[food[0]+1][food[1]]!=SPACE else obstacle
            # if food[0]+1<9 and board[food[0]+1][food[1]]==HUE:
            #      erase.appendleft([food[0]+1,food[1]]) 
            obstacle=(obstacle+1) if food[0]-1>=0 and board[food[0]-1][food[1]]!=SPACE else obstacle
            # if food[0]-1>=0 and board[food[0]-1][food[1]]==HUE:
            #      erase.appendleft([food[0]-1,food[1]]) 
            obstacle=(obstacle+1) if food[1]+1<14 and board[food[0]][food[1]+1]!=SPACE else obstacle
            # if food[1]+1<14 and board[food[0]][food[1]+1]==HUE:
            #      erase.appendleft([food[0],food[1]+1]) 
            obstacle=(obstacle+1) if food[1]-1>=0 and board[food[0]][food[1]-1]!=SPACE else obstacle
            # if food[1]-1>=0 and board[food[0]][food[1]-1]==HUE:
            #      erase.appendleft([food[0],food[1]-1]) 
            while obstacle>2:
                remove=hue
                empty_spaces= empty_spaces_list(board, SPACE)
                hue=random.choice(empty_spaces)
                print("uwu")
                board[hue[0]][hue[1]]=HUE
                board[remove[0]][remove[1]]=SPACE
            hue_list.appendleft(hue)
            hue_counter+=1
            if hue_counter>3:
                remove=hue_list.pop()
                while board[remove[0]][remove[1]]==SPACE:
                    remove=hue_list.pop()
                board[remove[0]][remove[1]]=SPACE
                hue_counter-=1
            score+=1
            speed= min(max_speed, speed*1.03)
        elif heading==BORDER:
            print('ALIEN HIT THE BORDER 💟!')
            break
        elif heading==HUE:
            print('ALIEN HIT THE 💢!')
            hoe=True
            break
        elif heading==BODY and head!=snake[-1]:
            print('ALIEN HIT ITSELF!👽')
            break

        if win == False :
            tail= snake.pop()
            board[tail[0]][tail[1]]=SPACE
        board[head[0]][head[1]]=HEAD
        board[last_head[0]][last_head[1]]=BODY
        last_head=head
        snake.appendleft(head)

        print(term.move_yx(0, 0))
        for row in board:
            print(''.join(row))
        
        if(score==0):
            print(f'score: {score} 😆 - speed: {speed:.1f}   ')
        else:
            print(f'score: {score} {FACE[score-1]} - speed: {speed:.1f}   ')
        if score==30:
            print("You won the game!🔥")
            break

if val.lower()=='q':
    print('You quit the game 😔!')
else:
    print('Game Over!')