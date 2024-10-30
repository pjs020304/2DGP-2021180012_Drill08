from pico2d import load_image, get_time
from state_machine import StateMachine, time_out, space_down, right_down, right_up, left_down, left_up, a_down


# 상태를 클래스를 통해서 정의함
class Idle:
    @staticmethod       # @는 데코레이터라 부름, 그 뒤에 오는 함수는 staticmethod라 보겠다. 멤버함수가 아님. 객체랑 상관없는 함수. 그룹화의 개념
    def enter(boy,e):        # self 파라미터를 안넣어줌
        boy.start_time = get_time()
        if left_up(e) or right_down(e) or boy.dir == -1:
            boy.action = 2
        elif right_up(e) or left_down(e)or boy.dir == 1:
            boy.action = 3
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time >5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy,e):
        boy.frame = 0
        if boy.action == 3:
            boy.theta = 1/2
        elif boy.action ==2:
            boy.theta = 1/2
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame*100, 300, 100, 100, 3.141592*boy.theta,'',boy.x-25,boy.y-25, 100,100)

class Run:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0

        if right_down(e) or left_up(e):
            boy.dir =1
            boy.action=1
        elif left_down(e) or right_up(e):
            boy.dir =-1
            boy.action = 0
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        if boy.x <=780 and boy.x >=20:
            boy.x += boy.dir*5
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame*100, boy.action*100, 100, 100,0,'',boy.x,boy.y, 100,100)

class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.dir = 1
        boy.action = 1
        boy.start_time = get_time()
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir*15
        boy.frame = (boy.frame + 1) % 8

        if boy.x >=780:
            boy.dir = -1
            boy.action = 0
        if boy.x<=20:
            boy.dir = 1
            boy.action = 1
        if get_time() - boy.start_time >5:
            boy.state_machine.add_event(('TIME_OUT', 0))
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame*100, boy.action*100, 100, 100,0,'',boy.x+25,boy.y+25, 200,200)



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.theta =0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.start_time=0
        self.state_machine.start(Idle)      # class를 파라미터로 보내줌
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, a_down: AutoRun},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                AutoRun: {right_down: Run, left_down: Run, time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event: 입력 이벤트
        # 우리가 state머신한테 넘겨줄건 튜플
        self.state_machine.add_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()
