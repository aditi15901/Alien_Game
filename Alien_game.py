from blessed import Terminal
import random
import copy
from collections import deque

random.seed(1)
term =Terminal()

UP = term.KEY_UP
DOWN = term.KEY_DOWN
LEFT = term.KEY_LEFT
RIGHT = term.KEY_RIGHT

BORDER ='💟'
BODY = '🌑' 
HEARTS = ('💗','💝','💖','💕','🤍','💜','💙','💚','🧡','💛')
SPACE ='  '
FACE= ('🗿','🙉','🙂','😀','🙈','🤌','😄','😁','😊','🥺','🥰','🌚','🥵','🥳','😏','🤩','🦄','😎','🌸','💯','🐻','🐼','🌷','🌝','✨','🔥','😱','🤯','😳','👑') #displayed with the score
HEAD='👽'
OBSTACLE='💢' # the obstacle which the alien should not hit

highscore=0 # stores the highscore for entire gameplay by player at a sitting

def empty_spaces_list(board, space): # returns a list of the empty spaces in the game zone that can be filled by a heart or obstacle
  list = []
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == space:
        list.append([i, j])
  return list

def update(board, remove, obs): 
    empty_spaces= empty_spaces_list(board, SPACE)
    obs=random.choice(empty_spaces)
    board[obs[0]][obs[1]]=OBSTACLE
    board[remove[0]][remove[1]]=SPACE
    return board,obs

print(term.home + term.clear)
print(term.white_on_black(('enter '+term.bold('n ')+term.normal+ 'to start game or '+term.bold('q ')+term.normal+'to quit gameplay')))
with term.cbreak(), term.hidden_cursor():
    value = term.inkey()
    while value.lower()!='q' and value.lower()!='n':
        value = term.inkey()
#print('enter n to start game or q to quit')
if value.lower()=='q':
    print(term.home + term.clear)
    print("you quit game 😔")

while value.lower()=='n':

    with term.cbreak(), term.hidden_cursor():  
        print(term.home + term.clear)
        print(term.bold('Highscore: '+term.normal+str(highscore))+term.normal) 

        alien = deque([[5,4],[5,3],[5,2]]) # initial alien position, the left-most being the head of the alien
        last_head=[5,4]                    # stores the position of the alien head at each move
        h,w=10, 15                         # the height and width of the game zone
        heart = [5,10]                     # initial position of food
        score = 0                          # stores the score of the player
        speed = 3                          # initial speed
        max_speed = 6                      # maximum speed for the alien
        last_heart=''                      # stores the last heart (as different hearts are used each time)
        heart_counter=0                    # stores the count for hearts to denote its positions in the heart list
        red_obstacles=0                    # stores the count of red obstacles (i.e. without counting the borders)
        obstacle_list=deque([])            # stores the positions of the red obstacles
        obstacle=0                         # stores the count of obstacles including the borders surrounding the current heart
        direction =RIGHT                   # stores intial direction of alien

        board = [[SPACE] * w for _ in range(h)]
        for i in range(h):
            board[i][0] = BORDER
            board[i][-1] = BORDER
        for j in range(w):
            board[0][j] = BORDER
            board[-1][j] = BORDER

        for s in alien:
            board[s[0]][s[1]] = BODY
            if s==alien[0]:
                board[s[0]][s[1]] = HEAD

        board[heart[0]][heart[1]] = HEARTS[0]
        last_heart=HEARTS[0]

        print(term.move_yx(2, 0))
        for row in board:
            print(''.join(row))
        print(term.move_down(1)+'use the arrow keys to move!')
        print('press q to quit')

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
            
            head = copy.copy(alien[0])

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
            if heading == last_heart:
                win=True
                empty_spaces= empty_spaces_list(board, SPACE)
                heart=random.choice(empty_spaces)
                if heart_counter==len(HEARTS)-1:
                    heart_counter=-1
                board[heart[0]][heart[1]]=HEARTS[(heart_counter+1)]
                last_heart=HEARTS[heart_counter+1]
                heart_counter+=1
                empty_spaces= empty_spaces_list(board, SPACE)
                obs=random.choice(empty_spaces) 
                last_obstacle=obs
                board[obs[0]][obs[1]]=OBSTACLE
                obstacle=0
                obstacle=1 if heart[0]+1<9 and board[heart[0]+1][heart[1]]!=SPACE else obstacle
                obstacle=(obstacle+1) if heart[0]-1>=0 and board[heart[0]-1][heart[1]]!=SPACE else obstacle
                obstacle=(obstacle+1) if heart[1]+1<14 and board[heart[0]][heart[1]+1]!=SPACE else obstacle
                obstacle=(obstacle+1) if heart[1]-1>=0 and board[heart[0]][heart[1]-1]!=SPACE else obstacle

                while (obstacle>2) or (head[0]+1<9 and board[head[0]+1][head[1]]==OBSTACLE)or (head[0]-1>=0 and board[head[0]-1][head[1]]==OBSTACLE) or (head[1]+1<14 and board[head[0]][head[1]+1]==OBSTACLE) or (head[1]-1>=0 and board[head[0]][head[1]-1]==OBSTACLE):
                    if (head[0]+1<9 and board[head[0]+1][head[1]]==OBSTACLE):
                        remove=(head[0]+1,head[1])
                        board,obs=update(board,remove,obs)
                    elif (head[0]-1>=0 and board[head[0]-1][head[1]]==OBSTACLE):
                        remove=(head[0]-1,head[1])
                        board,obs=update(board,remove,obs)
                    elif (head[1]+1<14 and board[head[0]][head[1]+1]==OBSTACLE):
                        remove=(head[0],head[1]+1)
                        board,obs=update(board,remove,obs)
                    elif (head[1]-1>=0 and board[head[0]][head[1]-1]==OBSTACLE):
                        remove=(head[0],head[1]-1)
                        board,obs=update(board,remove,obs)
                    elif obstacle>2:
                        remove=last_obstacle
                        board,obs=update(board,remove,obs)
                        obstacle-=1

                obstacle_list.appendleft(obs)
                red_obstacles+=1
                if red_obstacles>3:
                    remove=obstacle_list.pop()
                    while board[remove[0]][remove[1]]==SPACE:
                        remove=obstacle_list.pop()
                    board[remove[0]][remove[1]]=SPACE
                    red_obstacles-=1
                score+=1
                speed= min(max_speed, speed*1.2)
            elif heading==BORDER:
                print(term.clear_eol+term.move_up(1)+'ALIEN HIT THE BORDER 💟!     ')
                break
            elif heading==OBSTACLE:
                print(term.clear_eol+term.move_up(1)+'ALIEN HIT THE 💢!')
                break
            elif heading==BODY and head!=alien[-1] and score!=0:
                print(term.clear_eol+term.move_up(1)+'ALIEN HIT ITSELF 👽!      ')
                break

            if win == False :
                tail= alien.pop()
                board[tail[0]][tail[1]]=SPACE
            board[head[0]][head[1]]=HEAD
            board[last_head[0]][last_head[1]]=BODY
            last_head=head
            alien.appendleft(head)

            print(term.move_yx(2, 0))
            for row in board:
                print(''.join(row))
            
            if(score==0):
                print(term.move_down(1)+f'score: {score} 😆 - speed: {speed:.1f}   ')
                print(term.clear_eol)
            else:
                print(term.move_down(1)+f'score: {score} {FACE[score-1]} - speed: {speed:.1f}   ')
                print(term.clear_eol)
            if score==30:
                print("You won the game!🔥")
                break

        if val.lower()=='q':
            print('you quit the last game 😔!')
        else:
            print(term.firebrick('Game Over!'))

    highscore = max(score,highscore)
    print(term.white_on_black(('enter '+term.bold('n ')+term.normal+ 'to start game or '+term.bold('q ')+term.normal+'to quit gameplay')))

    with term.cbreak(), term.hidden_cursor():
        value = term.inkey()
        while value.lower()!='q' and value.lower()!='n':
            value = term.inkey()
    if value.lower()=='q':
        print(term.home + term.clear)
        print("you quit game 😔")
