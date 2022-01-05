from .Constant import Constant
from .Reservation import Reservation
from collections import defaultdict, deque
from random import randrange



class Schedule:
    
    def __init__(self, configuration):
        self._configuration = configuration
        
        self._fitness = 0

        
        slots_length = Constant.DAYS_NUM * Constant.DAY_HOURS * self._configuration.numberOfRooms
        self._slots = [deque() for _ in range(slots_length)]

        
        
        self._classes = defaultdict(Reservation)

        
        self._criteria = (self._configuration.numberOfCourseClasses * Constant.DAYS_NUM) * [False]
        
        self._diversity = 0.0
        self._rank = 0

    def copy(self, c, setup_only):
        if not setup_only:
            self._configuration = c.configuration
            
            self._slots, self._classes = c.slots, c.classes

            
            self._criteria = c.criteria

            
            self._fitness = c.fitness
            return self

        return Schedule(c.configuration)

    
    def makeNewFromPrototype(self):
        
        new_chromosome = self.copy(self, True)
        new_chromosome_slots, new_chromosome_classes = new_chromosome._slots, new_chromosome._classes

        
        classes = self._configuration.courseClasses
        nr = self._configuration.numberOfRooms
        DAYS_NUM, DAY_HOURS = Constant.DAYS_NUM, Constant.DAY_HOURS + 1
        for c in classes:
            
            dur = c.Duration
            day = randrange(32768) % DAYS_NUM
            room = randrange(32768) % nr
            time = randrange(32768) % (DAY_HOURS - dur)
            reservation = Reservation(nr, day, time, room)
            reservation_index = hash(reservation)

            
            for i in range(reservation_index, reservation_index + dur):
                new_chromosome_slots[i].append(c)

            
            new_chromosome_classes[c] = reservation

        new_chromosome.calculateFitness()
        return new_chromosome

    
    def crossover(self, parent, numberOfCrossoverPoints, crossoverProbability):
        
        if randrange(32768) % 100 > crossoverProbability:
            
            return self.copy(self, False)

        
        n = self.copy(self, True)
        n_classes, n_slots = n._classes, n._slots

        classes = self._classes
        
        size = len(classes)

        cp = size * [False]

        
        for i in range(numberOfCrossoverPoints, 0, -1):
            check_point = False
            while not check_point:
                p = randrange(32768) % size
                if not cp[p]:
                    cp[p] = check_point = True

        
        first = randrange(2) == 0        
        
        for i in range(size):
            if first:
                course_class = course_classes[i]
                dur = course_class.Duration
                reservation = classes[course_class]
                reservation_index = hash(reservation)
                
                n_classes[course_class] = reservation
                
                for i in range(reservation_index, reservation_index + dur):
                    n_slots[i].append(course_class)
            else:
                course_class = parent_course_classes[i]
                dur = course_class.Duration
                reservation = parent_classes[course_class]
                reservation_index = hash(reservation)
                
                n_classes[course_class] = reservation
                
                for i in range(reservation_index, reservation_index + dur):
                    n_slots[i].append(course_class)

            
            if cp[i]:
                
                first = not first

        n.calculateFitness()

        
        return n
        
    
    def crossovers(self, parent, r1, r2, r3, etaCross, crossoverProbability):
        
        size = len(self._classes)
        jrand = randrange(size)
        
        nr = self._configuration.numberOfRooms
        DAY_HOURS, DAYS_NUM = Constant.DAY_HOURS, Constant.DAYS_NUM

        
        new_chromosome = self.copy(self, True)
        new_chromosome_slots, new_chromosome_classes = new_chromosome._slots, new_chromosome._classes
        classes = self._classes
        course_classes = tuple(classes.keys())
        parent_classes = parent.classes
        parent_course_classes = tuple(parent.classes.keys())
        for i in range(size):
            if randrange(32768) % 100 > crossoverProbability or i == jrand:
                course_class = course_classes[i]                
                reservation1, reservation2, reservation3 = r1.classes[course_class], r2.classes[course_class], r3.classes[course_class]
                
                dur = course_class.Duration
                day = int(reservation3.Day + etaCross * (reservation1.Day - reservation2.Day))
                if day < 0:
                    day = 0
                elif day >= DAYS_NUM:
                    day = DAYS_NUM - 1
                    
                room = int(reservation3.Room + etaCross * (reservation1.Room - reservation2.Room))
                if room < 0:
                    room = 0
                elif room >= nr:
                    room = nr - 1
                    
                time = int(reservation3.Time + etaCross * (reservation1.Time - reservation2.Time))
                if time < 0:
                    time = 0
                elif time >= (DAY_HOURS + 1 - dur):
                    time = DAY_HOURS - dur
                    
                reservation = Reservation(nr, day, time, room)
                reservation_index = hash(reservation)

                
                for i in range(reservation_index, reservation_index + dur):
                    new_chromosome_slots[i].append(course_class)

                
                new_chromosome_classes[course_class] = reservation
            else:
                course_class = parent_course_classes[i]
                dur = course_class.Duration
                reservation = parent_classes[course_class]
                reservation_index = hash(reservation)
                
                
                for i in range(reservation_index, reservation_index + dur):
                    new_chromosome_slots[i].append(course_class)
                
                
                new_chromosome_classes[course_class] = reservation
                
        new_chromosome.calculateFitness()

        
        return new_chromosome

    
    def mutation(self, mutationSize, mutationProbability):
        
        if randrange(32768) % 100 > mutationProbability:
            return

        classes = self._classes
        
        numberOfClasses = len(classes)
        course_classes = tuple(classes.keys())
        configuration = self._configuration
        slots = self._slots
        nr = configuration.numberOfRooms

        DAY_HOURS = Constant.DAY_HOURS
        DAYS_NUM = Constant.DAYS_NUM

        
        for i in range(mutationSize, 0, -1):
            
            mpos = randrange(32768) % numberOfClasses

            
            cc1 = course_classes[mpos]
            reservation1 = classes[cc1]
            reservation1_index = hash(reservation1)

            
            dur = cc1.Duration
            day = randrange(32768) % DAYS_NUM
            room = randrange(32768) % nr
            time = randrange(32768) % (DAY_HOURS + 1 - dur)
            reservation2 = Reservation(nr, day, time, room)
            reservation2_index = hash(reservation2)

            
            for j in range(dur):
                
                cl = slots[reservation1_index + j]
                clTuple = tuple(cl)
                for cc1 in clTuple:
                    cl.remove(cc1)

                
                slots[reservation2_index + j].append(cc1)

            
            classes[cc1] = reservation2

        self.calculateFitness()

    
    def calculateFitness(self):
        
        score = 0

        criteria, configuration = self._criteria, self._configuration
        items, slots = self._classes.items(), self._slots
        numberOfRooms = configuration.numberOfRooms
        DAY_HOURS, DAYS_NUM = Constant.DAY_HOURS, Constant.DAYS_NUM
        daySize = DAY_HOURS * numberOfRooms

        ci = 0
        getRoomById = configuration.getRoomById

        
        for cc, reservation in items:
            
            day, time, room  = reservation.Day, reservation.Time, reservation.Room

            dur = cc.Duration

            
            reservation_index = hash(reservation)
            cls = slots[reservation_index: reservation_index + dur]
            ro = any(filter(lambda slot: len(slot) > 1, cls))

            
            score = 0 if ro else score + 1

            criteria[ci + 0] = not ro

            r = getRoomById(room)
            
            criteria[ci + 1] = r.NumberOfSeats >= cc.NumberOfSeats
            score = score + 1 if criteria[ci + 1] else score / 2

            
            criteria[ci + 2] = (not cc.LabRequired) or (cc.LabRequired and r.Lab)
            score = score + 1 if criteria[ci + 2] else score / 2

            po = go = False

            
            t = day * daySize + time
            professorOverlaps, groupsOverlap = cc.professorOverlaps, cc.groupsOverlap
            try:
                for k in range(numberOfRooms, 0, -1):
                    
                    for i in range(t, t + dur):
                        cl = slots[i]
                        for cc1 in cl:
                            if cc != cc1:
                                
                                if not po and professorOverlaps(cc1):
                                    po = True
                                
                                if not go and groupsOverlap(cc1):
                                    go = True
                                
                                if po and go:
                                    raise Exception('no need to check more')

                    t += DAY_HOURS
            except Exception:
                pass

            
            score = 0 if po else score + 1

            criteria[ci + 3] = not po

            
            score = 0 if go else score + 1

            criteria[ci + 4] = not go
            ci += DAYS_NUM

        
        self._fitness = score / (configuration.numberOfCourseClasses * DAYS_NUM)

    
    @property
    def fitness(self):
        return self._fitness

    @property
    def configuration(self):
        return self._configuration

    @property
    
    def classes(self):
        return self._classes

    @property
    
    def criteria(self):
        return self._criteria

    @property
    
    def slots(self):
        return self._slots
        
    @property
    def diversity(self):
        return self._diversity

    @diversity.setter
    def diversity(self, new_diversity):
        self._diversity = new_diversity
        
    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, new_rank):
        self._rank = new_rank
        
    def __hash__(self) -> int:
        prime = 31
        result = 1
        classes = self._classes
        for cc in classes.keys():
            reservation = classes[cc]
            result = prime * result + (0 if reservation is None else hash(reservation))
        return result

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        classes = self._classes
        for cc in classes.keys():
            if classes[cc] != other.classes[cc]:
                return False
            
    def __ne__(self, other):
        return not self.__eq__(other)
