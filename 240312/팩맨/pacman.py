# 몬스터 : [x, y, 바라보고 있는 방향]
# 여러개 있을 수 있으니 리스트 형태로 관리 해야함
# 시체보드 :
# 알 보드 :
# 전체 보드
from collections import deque

m, t = map(int , input().split())
monster_board = [
    [[] for _ in range(4)]
    for _ in range(4)
]

egg_board = [
    [[] for _ in range(4)]
    for _ in range(4)
]
# packman dir
# 턴이 끝나게 되면 i, j 위치에 dir을 가진 팩맨을 몬스터 보드에 추가해준다,
# 여러개가 있을 수 있기에 추가한다.

die_board = [
    [0 for _ in range(4)]
    for _ in range(4)
]
# 2, 1, 0.. 0이 되면 시체는 없는 걸로!
# 여러개가 있어도 어차피 갱신이 되면 되기에 리스트 필요 X

# 위.. 반시계 방향으로 증가
m_dx = [-1, -1, 0, 1, 1, 1, 0, -1]
m_dy = [0, -1, -1, -1, 0, 1, 1, 1]

# 우 하 좌 상 # 숫자 큰게 자연스럽게 우선 순위 되게 하기 위해
p_dx = [-1, 0, 1, 0]
p_dy = [0, -1, 0, 1]

# 팩맨 움직임 리스트
p_moving_list = []
"""
# 1. 몬스터보드 각 i, j를 조사해 dir을 해당 에그보드에 추가
# 2. 몬스터보드 각 i, j를 조사해 가진 dir, dir + 1 .. 로 갈 수 있는 방향이 나올 때 까지 조사 % 8 필요
# 2.0 새로운 몬스터보드를 (nextboard)를 생성해서 추가를 해야함
# 2.1 만약 카운트가 8까지 되면 갈 수 있는 방향이 없기에 그 자리에 추가

# 3. 팩맨이동을 하는데, p_dx,dy 기준으로 움직이며 
# 3.1 tuple 비교를 통해 (먹은 개수, 첫번쨰 방향, 두번째 방향, 세번째 방향) 을 최신화 하낟
# 3.2 먹을 때 실제로 반영하지 않고 카운트만 하고(len) , 64개 한 최종 결과가 나온다면
# 3.3 저 tuple[1, 2, 3] 을 기준으로 행동해서 먹는다.
# 4. 먹은 위치를 기준으로 시체보드에 2를 넣는다. 

# 5. 에그보드에 있는 값을 모두 다시 몬스터 보드에 추가하고
# 5.1 에그보드를 초기화 한다
"""

# Input
r, c = map(int , input().split()) # 팩맨 위치
r += -1
c += -1

visited = [
    [False for _ in range(4)]
    for _ in range(4)
]

for _ in range(m) :
    x, y, dir = map(int, input().split())
    x += -1
    y += -1
    dir += -1
    monster_board[x][y].append( [x, y, dir])

# print(*monster_board,sep='\n')
def in_range(x, y) :
    return 0 <= x < 4 and 0 <= y < 4


def make_egg() :
    global monster_board
    global egg_board

    # for i in range(4) :
    #     for j in range(4) :
    #         egg_board[i][j] = []
    # 1. 몬스터보드 각 i, j를 조사해 dir을 해당 에그보드에 추가
    for i in range(4):
        for j in range(4) :
            if monster_board[i][j] :
                for mon in monster_board[i][j] :
                    egg_board[i][j].append(mon[2]) # mon2 : dir

    # print("에그 생성현황")
    # print(*egg_board, sep='\n')


def monster_move() :
    global monster_board
    global egg_board
    global r, c

    next_monster_board = [
        [ [] for _ in range(4) ]
        for _ in range(4)
    ]
    # 2. 몬스터보드 각 i, j를 조사해 가진 dir, dir + 1 .. 로
    # 갈 수 있는 방향이 나올 때 까지 조사 % 8 필요
    # 2.0 새로운 몬스터보드를 (nextboard)를 생성해서 추가를 해야함
    # 2.1 만약 8까지 되면 갈 수 있는 방향이 없기에 그 자리에 추가
    # 2.2 그전에 추가된다면 break를 통해 다음 몬스터 고르기!

    flag = False
    for i in range(4):
        for j in range(4) :
            if monster_board[i][j] :
                # print(monster_board[i][j])
                for mon in monster_board[i][j] :
                    flag = False
                    for k in range(8) :
                        move_dir = (mon[2] + k) % 8
                        nx = i + m_dx[move_dir]
                        ny = j + m_dy[move_dir]
                        # print(nx, ny)
                        if not in_range(nx, ny) : continue
                        if die_board[nx][ny] != 0 : continue # 시체에는 못가요
                        if nx == r and ny == c : continue
                        # 갈 수 있다면
                        # print("몬스터이동 : ", nx, ny, move_dir)
                        next_monster_board[nx][ny].append([nx, ny, move_dir])
                        flag = True
                        break

                    if flag == False :
                        # 갈 수 있는 곳이 없다면 원래 위치에 원래의 값 그대로 추가
                        next_monster_board[i][j].append([i, j, mon[2]])

    # print(*next_monster_board, sep='\n')
    # print("위는 다음 보드임")
    # 원본으로 복사!
    for i in range(4) :
        for j in range(4) :
            monster_board[i][j] = next_monster_board[i][j]

    # monster_board = copy.deepcopy(next_monster_board)
    # print(*monster_board, sep='\n')

eat_board = [
    [ [] for _ in range(4) ]
    for _ in range(4)
]

def dfs(depth, x, y, state, eat) :
    global monster_board
    global visited
    global eat_board

    for i in range(4) :
        for j in range(4) :
            eat_board[i][j] = monster_board[i][j]

    eat_board = copy.deepcopy(monster_board)
    eat_flag = False
    # print("DFS하는 보드")
    # print(*monster_board,sep='\n')
    if depth == 3 :
        # print(eat, state)
        temp = (eat, state[0], state[1], state[2])
        p_moving_list.append(temp)
        return

    for i in range(4) :
        nx = x + p_dx[i]
        ny = y + p_dy[i]

        if not in_range(nx, ny) : continue
        if monster_board[nx][ny] :
            if not visited[nx][ny] :
                eat += len(monster_board[nx][ny])
                eat_flag = True
                visited[nx][ny] = True

        state.append(i)
        dfs(depth + 1, nx, ny, state, eat)
        if eat_flag == True :
            eat += -len(monster_board[nx][ny])
        # visited[nx][ny] = False
        state.pop()


# 3. 팩맨이동을 하는데, p_dx,dy 기준으로 움직이며
# 3.1 tuple 비교를 통해 (먹은 개수, 첫번쨰 방향, 두번째 방향, 세번째 방향) 을 최신화 하낟
# 3.2 먹을 때 실제로 반영하지 않고 카운트만 하고(len) , 64개 한 최종 결과가 나온다면
# 3.3 저 tuple[1, 2, 3] 을 기준으로 행동해서 먹는다.
# 4. 먹은 위치를 기준으로 시체보드에 2를 넣는다.

def kill_monster(tu) :
    global r, c
    x, y = r, c
    killed_num = 0

    v_pos = set()

    for i in tu :
        nx = x + p_dx[i]
        ny = y + p_dy[i]

        if not in_range(nx, ny) :
            return -1

        if (nx, ny) not in v_pos :
            killed_num += len(monster_board[nx][ny])
            v_pos.add((nx, ny))

        x, y = nx, ny

    return killed_num


def packman_move() :
    global monster_board
    global die_board
    global r,c
    global p_moving_list
    global visited
    global eat_board

    best_case = (0, 0, 0)
    eat_cnt = 0
    # bfs 리턴으로 저 값을 가져와 비교한다.

    # 안될거 같으니 3중 포문하자 그냥 모든 시간은 똑같다.
    # print(*monster_board,sep='\n')
    for i in range(4) :
        for j in range(4) :
            for k in range(4) :
                now_tuple = (i, j, k)

                now_eat_cnt = kill_monster(now_tuple)

                if now_eat_cnt > eat_cnt :
                    eat_cnt = now_eat_cnt
                    best_case = (now_tuple[0], now_tuple[1], now_tuple[2])

    # for i in range(4) :
    #     for j in range(4) :
    #         visited[i][j] = False
    #
    # p_moving_list = []
    # dfs(0, r, c, [], 0)
    # for nc in p_moving_list :
    #     if nc > best_case :
    #         best_case = nc
    #     print("nc", nc)
    # # if now_case > best_case :
    # #     best_case = now_case

    # print("먹기 직전")
    # print(*monster_board,sep='\n')
    # 이제 순서대로 먹기~

    x, y = r, c
    for dir in best_case :
        x = x + p_dx[dir]
        y = y + p_dy[dir]

        if monster_board[x][y] :
            # monster_board[x][y].clear()
            # print("제거")
            monster_board[x][y] = []
            die_board[x][y] = 3

    r, c = x, y
    # print("팩맨 위치", r, c)

def egg_bohwal() :
    global egg_board
    global monster_board

    # 5. 에그보드에 있는 값을 모두 다시 몬스터 보드에 추가하고
    # 5.1 에그보드를 초기화 한다
    # print("eggggggg")
    # print(*egg_board, sep='\n')
    # print("eggggggg")
    for i in range(4):
        for j in range(4) :
            if egg_board[i][j] :
                for egg in egg_board[i][j] :
                    monster_board[i][j].append([i, j,egg]) # mon2 : dir

    for i in range(4) :
        for j in range(4) :
            egg_board[i][j] = []


def die_minus() :
    global die_board

    for i in range(4):
        for j in range(4):
            if die_board[i][j] > 0 :
                die_board[i][j] += -1

answer = 0
def get_monster() :
    global monster_board
    global answer

    for i in range(4):
        for j in range(4):
            if monster_board[i][j] :
                answer += len(monster_board[i][j])

for _ in range(t) :
    make_egg()
    monster_move()
    packman_move()
    die_minus()
    egg_bohwal()

get_monster()
# print(*monster_board,sep='\n')
print(answer)

#
# def bfs(a,b) :
#     global visited, monster_board
#     q = deque()
#     q.append((a, b, 0, 0))
#     visited[a][b] = True
#     eat_moving_tuple = (0,0,0,0)
#     while q :
#         x, y, eat, cnt = q.popleft()
#         if cnt == 3 :
#             pass
#
#         for i in range(4) :
#             nx = x + p_dx[i]
#             ny = y + p_dy[i]
#
#             if not in_range(nx, ny) : continue