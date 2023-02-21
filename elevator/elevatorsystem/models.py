from django.db import models

# Create your models here.


class Elevator(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('maintenance', 'Under Maintenance')
    ]
    STATUS_MAP = {
        'available': 0,
        'busy': 1,
        'maintenance': 2
    }

    floor = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='available', max_length=20)
    # 0 for stationary, 1 for up and -1 for down
    direction = models.IntegerField(default=0)
    requests = models.JSONField(default=list)

    def open_door(self):
        self.status = 'busy'
        self.save()

    def close_door(self):
        self.status = 'available'
        self.save()

    def move(self):
        if not self.requests:
            return

        # TODO: optimize it further
        self.requests.sort()
        next_floor = self.requests.pop(0)

        if next_floor > self.floor:
            self.direction = 1
            self.floor = next_floor
        elif next_floor < self.floor:
            self.direction = -1
            self.floor = next_floor
        else:
            self.direction = 0
        self.save()

    def stop(self):
        self.direction = 0
        self.save()

    def display(self):
        return f"Elevator id:{self.id} and statusL:{self.status}"
