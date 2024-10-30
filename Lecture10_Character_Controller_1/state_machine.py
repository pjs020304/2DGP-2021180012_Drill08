from sdl2 import *
# 이벤트 체크함수
# 상태 이벤트 e = (종료, 실제값) 튜플로 정의


def start_event(e):
    pass

def space_down(e): # e가 space down 인지 판단
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
    pass
def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a







class StateMachine:
    def __init__(self, obj):
        self.obj = obj      # 어떤 객체를 위한 상태머신인지 알려줌
        self.event_que = [] # 상태 이벤트를 보관할 큐
        pass
    def start(self, state):
        print(f'Enter into {state}')
        self.cur_state = state      # 시작 상태를 받아서 그걸로 현재 상태로 만듦
        pass
    def update(self):
        self.cur_state.do(self.obj)

        # 이벤트가 있으면 상태 바꾸기
        if self.event_que: # list는 멤버가 있으면 True
            e = self.event_que.pop(0)
            # 이 시점에서 우리한테 주어진 정보는?
            # e와 cur_state
            # 다음 상태를 결정해야됨
            # -> 상태변환 테이블을 이용
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    print(f'Exit from {self.cur_state}')
                    self.cur_state.exit(self.obj,e)
                    self.cur_state = next_state
                    self.cur_state.enter(self.obj,e)
                    print(f'Enter into {next_state}')
                    return

            # 이 시점에 왔다는 것은 event에 따른 전환 문제
            print(f'        WARNING: {e} not handled at state {self.cur_state}')





    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def add_event(self, e):
        print(f'    DEBUG: add event {e}')
        self.event_que.append(e)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

