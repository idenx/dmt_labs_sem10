#!/usr/bin/env python3
import random

class Bunch(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __repr__(self):
        return repr(self.__dict__)

class Car(object):
    SPEED_PER_ACCEL = 0.1
    STEP_PER_SPEED = 1.0
    START_HEALTH = 1.0
    MIN_HEALTH = 0.01
    MAX_DIST_TO_ATTACK = 3.0
    MAX_CONTROL = 10.0

    MIN_SPEED_LOSS = 0.1
    MIN_HEALTH_LOSS = 0.05

    SUCCESS_ATTACK_SELF_SPEED_LOSS_COEF = 0.95
    SUCCESS_ATTACK_RIVAL_SPEED_LOSS_COEF = 0.5
    SUCCESS_ATTACK_SELF_HEALTH_LOSS = 0.95
    SUCCESS_ATTACK_RIVAL_HEALTH_LOSS = 0.7

    FAILED_ATTACK_SELF_SPEED_LOSS_COEF = 0.95
    MIN_SUCCESSFULL_ATTACK_PROBABILITY = 0.2

    ATTACK_STRATEGIES = {
            'first': lambda _, rivals: sorted(rivals, key=lambda r: r.pos, reverse=True),
            'nearest': lambda _, rivals: sorted(rivals, key=lambda r: r.dist),
            'highest_success_attack_prob': lambda self, rivals: sorted(rivals, key=lambda r: self.get_successfull_attack_probability(r), reverse=True),
            'highest_top_speed': lambda _, rivals: sorted(rivals, key=lambda r: r.car.top_speed, reverse=True),
            'highest_cur_speed': lambda _, rivals: sorted(rivals, key=lambda r: r.car.cur_speed, reverse=True),
            'highest_acceleration': lambda _, rivals: sorted(rivals, key=lambda r: r.car.acceleration, reverse=True),
    }

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.cur_speed = 0
        self.health = self.START_HEALTH

    def get_offense_power(self):
        return self.strength * self.cur_speed * self.health * self.control
    def get_defense_power(self):
        return self.durability * self.cur_speed * self.health * self.control
    def get_successfull_attack_probability(self, rival):
        my_offense, rival_defense = self.get_offense_power(), rival.car.get_defense_power()
        return (1 - rival.dist / self.MAX_DIST_TO_ATTACK) * ((my_offense - rival_defense) / (my_offense + rival_defense + 1e-5))
    def attack(self, rival):
        sucess_probability = self.get_successfull_attack_probability(rival)
        if sucess_probability <= self.MIN_SUCCESSFULL_ATTACK_PROBABILITY:
            return True
        if random.random() < sucess_probability:
            self_speed_loss = min(self.cur_speed, max(self.cur_speed * (1 - self.SUCCESS_ATTACK_SELF_SPEED_LOSS_COEF), self.MIN_SPEED_LOSS))
            self.cur_speed -= self_speed_loss

            rival_speed_loss = min(rival.car.cur_speed, max(rival.car.cur_speed * (1 - self.SUCCESS_ATTACK_RIVAL_SPEED_LOSS_COEF), self.MIN_SPEED_LOSS))
            rival.car.cur_speed -= rival_speed_loss

            self_health_loss = min(self.health, max(self.health * (1 - self.SUCCESS_ATTACK_SELF_HEALTH_LOSS), self.MIN_HEALTH_LOSS))
            self.health -= self_health_loss

            rival_health_loss = min(rival.car.health, max(rival.car.health * (1 - self.SUCCESS_ATTACK_RIVAL_HEALTH_LOSS), self.MIN_HEALTH_LOSS))
            rival.car.health -= rival_health_loss

            print('  -- "{}" attacked "{}" (speed loss = {:.2f}, health loss={:.2f}, prob={:.2f})'.format(
                  self.name, rival.car.name, rival_speed_loss, rival_health_loss, sucess_probability))
            return True
        else:
            self_speed_loss = min(self.cur_speed, max(self.cur_speed * (1 - self.FAILED_ATTACK_SELF_SPEED_LOSS_COEF), self.MIN_SPEED_LOSS))
            self.cur_speed -= self_speed_loss
            #print('  --- "{}" failed to attack "{}" (speed loss={:.2f}, prob={:.2f})'.format(
            #      self.name, rival.car.name, self_speed_loss, sucess_probability))
            return False

    def is_alive(self):
        return self.health > self.MIN_HEALTH

    def make_move_step(self, is_turn):
        if not self.is_alive():
            return 0

        if is_turn:
            self.cur_speed *= self.control / self.MAX_CONTROL
        elif self.cur_speed < self.top_speed:
            old_speed = self.cur_speed
            self.cur_speed = min(self.top_speed, self.cur_speed + self.acceleration * self.SPEED_PER_ACCEL)
        return self.cur_speed * self.STEP_PER_SPEED

    def make_attack_step(self, rivals):
        if not self.is_alive():
            return
        rivals_can_attack = [r for r in rivals if r.dist < self.MAX_DIST_TO_ATTACK]
        rivals_to_attack = self.ATTACK_STRATEGIES[self.at_strategy](self, rivals_can_attack)
        for rival in rivals_to_attack:
            if not self.attack(rival):
                break

    def state_to_str(self):
        if not self.is_alive():
            return 'crashed'
        return 'speed={:.2f}, health={:.2f}, off={:.2f}, def={:.2f}'.format(
                self.cur_speed, self.health, self.get_offense_power(), self.get_defense_power())
    def __repr__(self):
        return 'Car(name={}, cur_sp={:.2f}, h={:.2f})'.format(self.name, self.cur_speed, self.health)

class Race(object):
    TURNS_DENSITY = 0.1

    def __init__(self, cars, track_len):
        self._cars = cars
        random.shuffle(self._cars)
        self._track_len = track_len
        self._car_positions = [0 for _ in range(track_len)]
    def make_step(self):
        is_turn = random.random() < self.TURNS_DENSITY
        if is_turn:
            print('turn on the track!')

        for i, car in enumerate(self._cars):
            self._car_positions[i] += car.make_move_step(is_turn)

        for i, car in enumerate(self._cars):
            distances = map(lambda p: abs(self._car_positions[i] - p), self._car_positions)
            rivals = tuple(Bunch(car=c, dist=d, pos=p) for c, d, p in zip(self._cars, distances, self._car_positions) if c != car)
            car.make_attack_step(rivals)

        return all(pos < self._track_len for pos in self._car_positions) and any(car.is_alive() for car in self._cars)
    def get_winner(self):
        return max(zip(self._cars, self._car_positions), key=lambda v: v[1])[0]
    def print_state(self):
        for i, (car, pos) in enumerate(sorted(zip(self._cars, self._car_positions), key=lambda v: v[1], reverse=True)):
            print('#{}: {:.1f}/{} passed, {}: {}'.format(i + 1, min(self._track_len, pos), self._track_len, car.name, car.state_to_str()))

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        random.seed(int(sys.argv[1]))
    cars = [
#        Car(name='Jaguar C-X75', top_speed=8.6, acceleration=8.5, control=8.3, strength=4.2, durability=3.8),
        Car(name='Ferrari Enzo (nearest)', top_speed=8.4, acceleration=8.1, control=4.8, strength=2.3, durability=3.6, at_strategy='nearest'),
        Car(name='Audi R8 (first)', top_speed=6.1, acceleration=6.9, control=5.7, strength=7.4, durability=4.0, at_strategy='first'),
        Car(name='BMW M3 GTS (succ prob)', top_speed=5.6, acceleration=7.8, control=6.2, strength=7.3, durability=4.8, at_strategy='highest_success_attack_prob'),
        Car(name='Ford Mustang GT (top speed)', top_speed=6.0, acceleration=5.8, control=8.0, strength=6.4, durability=7.8, at_strategy='highest_top_speed'),
        Car(name='Lamborghini Galardo (cur speed)', top_speed=6.7, acceleration=6.6, control=6.0, strength=3.4, durability=3.0, at_strategy='highest_cur_speed'),
        Car(name='Maserati GranTurismo (accel)', top_speed=4.2, acceleration=8.0, control=3.9, strength=6.7, durability=4.2, at_strategy='highest_acceleration'),
    ]

    race = Race(cars=cars, track_len=100)

    race.print_state()
    print('')
    i = 0
    r = True
    while r:
        i += 1
        print('Step #{}\n'.format(i) + '-' * 80)
        r = race.make_step()
        race.print_state()
        print('')
    print('Winner: {}'.format(race.get_winner().name))
    import os
    os.system('say "Машина {} выиграла гонку!"'.format(race.get_winner().name))
