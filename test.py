import time
timer = 0.5 * 60

while timer > 0:
    time.sleep(0.985)
    timer -= 1
    print("I still wont execute...")

print("Now I will reset the timer")
timer = 0.5 * 60