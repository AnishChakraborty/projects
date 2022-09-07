import random
def play():
    user = input("choose any of one rock - r  paper - p scissor - s ")
    machine_choice = random.choice(['r','p','s'])
    print(f'machine_choice was {machine_choice}')
    if user == machine_choice:
        return "tie"
    elif (user == 'r' and machine_choice == 'p') or (user == "s" and machine_choice == "r") or (user == "s" and machine_choice == 'r'):
        return 'machine wins'
    else:
        return 'player wins'
    
ans = play()
print(ans)